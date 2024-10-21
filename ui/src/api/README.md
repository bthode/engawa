openapi-generator-cli generate -i http://127.0.0.1:8000/openapi.json -g typescript-fetch -o .
rm index.ts
fd --extension ts --exec sed -i '' '/tslint:disable/d' {}

