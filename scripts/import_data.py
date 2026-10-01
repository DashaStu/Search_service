import csv
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Document as DocumentORM
from app.database import DATABASE_URL
from app.search import es_client
from datetime import datetime
from sqlalchemy import select
from app.database import Base

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def import_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(DocumentORM).limit(1))
        if result.scalar():
            print("Данные уже загружены, пропускаем.")
            return
        with open("data/posts.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rubrics_list = [r.strip() for r in row['rubrics'].split(',')]
                
                doc = DocumentORM(
                    rubric=rubrics_list, 
                    text=row['text'],
                    created_at=datetime.fromisoformat(row['created_date'])
                )
                session.add(doc)
                await session.flush() 
                
                await es_client.index(
                    index="documents",
                    id=doc.id,
                    document={"text": row['text']}
                )
                await session.commit()

        
        print("Импорт завершен!")

if __name__ == "__main__":
    asyncio.run(import_data())