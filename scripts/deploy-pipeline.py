#!/usr/bin/env python3
"""
OpenShift CI/CD Setup Script
Automates the deployment of Tekton pipelines and ArgoCD applications
"""

import subprocess
import sys
import time

def run_command(command, description):
    """Execute shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("🚀 Starting OpenShift CI/CD Setup")
    
    # Create project/namespace
    run_command("oc new-project cicd-demo || oc project cicd-demo", 
                "Creating project")
    
    # Apply pipeline tasks
    run_command("oc apply -f pipelines/tasks/", 
                "Deploying pipeline tasks")
    
    # Apply main pipeline
    run_command("oc apply -f pipelines/pipeline.yaml", 
                "Deploying main pipeline")
    
    # Apply triggers
    run_command("oc apply -f pipelines/trigger.yaml", 
                "Setting up pipeline triggers")
    
    # Create service account with proper permissions
    run_command("""
    oc create serviceaccount pipeline || true
    oc adm policy add-scc-to-user privileged -z pipeline
    oc adm policy add-role-to-user edit -z pipeline
    """, "Setting up service account")
    
    # Deploy ArgoCD application
    run_command("oc apply -f argocd/application.yaml", 
                "Deploying ArgoCD application")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Push your code to GitHub")
    print("2. Set up GitHub webhook to trigger pipeline")
    print("3. Watch the pipeline run: oc get pipelineruns -w")
    print("4. Check ArgoCD sync status")

if __name__ == "__main__":
    main()