from typing import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middleware.db.postgresql import init_db
from configs.configs import settings
from utils.response_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("server is starting...")
    await init_db()
    yield
    print("server is stopping...")


def create_app():
    app = FastAPI(
        title="Blog Service",
        version="0.1.0",
        description="A simple web service for a blog application",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    from resources.users import router as users_router
    from resources.admin.tags import router as admin_tags_router
    app.include_router(users_router, prefix=settings.ROUTER_PREFIX)
    app.include_router(admin_tags_router, prefix=settings.ROUTER_PREFIX)

    for route in app.routes:
        print(f"{route.path} -> {','.join(route.methods)}")

    return app


app = create_app()

# @app.ad("/api/tags")
# async def get_tags():
#     import os
#     import sys
#     import json
#
#     root_dir = os.path.dirname(os.path.abspath(__file__))
#
#     sys.path.insert(0, root_dir)
#     blog_file = os.path.join(root_dir, "data", "_index.json")
#
#     with open(blog_file, "r", encoding="utf-8") as f:
#         blogs = json.load(f)
#
#     tags = [blog["tags"] for blog in blogs]
#     tags = [tag for tag_list in tags for tag in tag_list]
#     from collections import Counter
#     tag_count = Counter(tags)
#
#     return dict(tag_count)
#
#
# @app.get("/api/blogs", response_model=BlogListEntity)
# async def get_blogs(request: Annotated[BlogRequest, Query()]):
#     """
#     获取全部博客列表
#     """
#
#     import os
#     import sys
#     import json
#
#     root_dir = os.path.dirname(os.path.abspath(__file__))
#
#     sys.path.insert(0, root_dir)
#     blog_file = os.path.join(root_dir, "data", "_index.json")
#
#     with open(blog_file, "r", encoding="utf-8") as f:
#         blogs = json.load(f)
#
#     if request.tag:
#         blogs = [blog for blog in blogs if request.tag in blog["tags"]]
#
#     total = len(blogs)
#
#     start = (request.page - 1) * request.page_size
#     end = start + request.page_size
#
#     return {"blogs": blogs[start:end], "total": total}

