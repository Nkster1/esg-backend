dev-run:
	 uvicorn main:app --reload
prod-run:
	uvicorn main:app --host 0.0.0.0 --port 8000

build:
	docker build  -t ghcr.io/nkster1/esg-pilot-backend .
push:
	docker push ghcr.io/nkster1/esg-pilot-backend
run:
	docker run  --rm  -d -p 8000:8000  --env OPENAI_API_KEY='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' ghcr.io/nkster1/esg-pilot-backend