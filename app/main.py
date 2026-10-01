from fastapi import FastAPI, Depends, status
from app.database import engine, Base, get_db
from app.search import init_index, es_client
from app.models import Document as DocumentORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.schemas import SDocumentBase as DocumentSchema



app = FastAPI()
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Service is running"}

@app.get("/search", response_model=list[DocumentSchema])
async def search(query: str, db: AsyncSession = Depends(get_db)):
    resp = await es_client.search(
        index="documents",
        query={"match": {"text": query}},
        size=20
    )
    
    ids = [int(hit["_id"]) for hit in resp["hits"]["hits"]]
    
    if not ids:
        return []

    result = await db.execute(select(DocumentORM).where(DocumentORM.id.in_(ids)))
    docs = result.scalars().all()
    
    docs.sort(key=lambda x: x.created_at, reverse=True)
    
    return docs


@app.delete("/documents/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(DocumentORM).where(DocumentORM.id == id))
    await db.commit()
    try:
        await es_client.delete(index="documents", id=str(id), ignore=[404])
    except:
        # Здесь в реальности мы должны отправить задачу в очередь (RabbitMQ/Kafka)
        # для последующего удаления
        print(f"CRITICAL: Failed to delete document {id} from Elasticsearch")
    
    return None