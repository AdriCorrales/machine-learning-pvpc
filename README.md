# machine-learning-pvpc
Repository for the machine learning energy prices predictions. Front and back end code.

Requirements:
1. Have Docker Desktop installed
2. Have Kubernetes enabled
3. Have Kubectl installed

Steps:
1. Download "models.yaml", "backend-deployment.yaml" and "backend-service.yaml"
2. Execute "kubectl apply -f models.yaml"
3. Execute "kubectl apply -f backend-deployment.yaml"
4. Execute "kubectl apply -f backend-service.yaml"

Web API should be running at 127.0.0.1:30036 endpoint