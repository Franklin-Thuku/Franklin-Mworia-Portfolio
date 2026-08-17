import asyncio
import httpx


async def test_api():
    print("Testing FastAPI endpoints...")
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        # 1. Health check
        res_health = await client.get("/health")
        print("Health Check:", res_health.status_code, res_health.json())
        assert res_health.status_code == 200

        # 2. List projects
        res_projects = await client.get("/api/v1/projects")
        print("List Projects:", res_projects.status_code, f"Found {len(res_projects.json())} projects")
        assert res_projects.status_code == 200
        assert len(res_projects.json()) >= 4

        # 3. Filter projects by category
        res_filtered = await client.get("/api/v1/projects?category=ai")
        print("Filter Projects (AI):", res_filtered.status_code, f"Found {len(res_filtered.json())} projects")
        assert res_filtered.status_code == 200

        print("All Phase 1 tests passed successfully!")


if __name__ == "__main__":
    asyncio.run(test_api())
