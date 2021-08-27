# main.py
from fastapi import FastAPI, Form, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from app.models import Job
from pydantic import BaseModel

class Status(BaseModel):
    message: str

app = FastAPI()

job_pydantic_all_fields = pydantic_model_creator(Job)
job_pydantic = pydantic_model_creator(Job, exclude_readonly=True)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/job/create/", status_code=201)
async def create_job(name=Form(...), description=Form(...)):
    job = await Job.create(name=name, description=description)
    return await job_pydantic.from_tortoise_orm(job)

@app.get("/jobs/")
async def get_jobs():
    return await job_pydantic.from_queryset(Job.all())


@app.put("/job/{job_id}", response_model=job_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_job(job_id: int, job: job_pydantic):
    await Job.filter(id=job_id).update(**job.dict())
    return await job_pydantic.from_queryset_single(Job.get(id=job_id))

@app.get("/job/{job_id}", response_model=job_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_job(job_id: int):
    return await job_pydantic.from_queryset_single(Job.get(id=job_id))

@app.delete("/job/{job_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_job(job_id: int):
    deleted_job = await Job.filter(id=job_id).delete()
    if not deleted_job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return Status(message=f"Deleted job {job_id}")

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)