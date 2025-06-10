#!/usr/bin/env python3
"""
GitHub Webhook Setup Script
Configures GitHub webhook to trigger OpenShift pipelines
"""

import requests
import json
import sys
import subprocess

def get_webhook_url():
    """Get the EventListener route URL"""
    try:
        result = subprocess.run(
            "oc get route el-flask-app-listener -o jsonpath='{.spec.host}'",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            return f"https://{result.stdout.strip()}"
        else:
            # Create route if it doesn't exist
            subprocess.run("""
            oc expose service el-flask-app-listener \
              --name=el-flask-app-listener \
              --hostname=$(oc get route -o jsonpath='{.items[0].spec.host}' | sed 's/[^.]*\./webhook\./')
            """, shell=True)
            return get_webhook_url()
    except Exception as e:
        print(f"Error getting webhook URL: {e}")
        return None

def main():
    webhook_url = get_webhook_url()
    if webhook_url:
        print(f"🔗 Webhook URL: {webhook_url}")
        print("\nTo complete setup:")
        print("1. Go to your GitHub repository settings")
        print("2. Navigate to Webhooks")
        print("3. Add webhook with:")
        print(f"   - Payload URL: {webhook_url}")
        print("   - Content type: application/json")
        print("   - Events: Push events")
    else:
        print("❌ Could not determine webhook URL")

if __name__ == "__main__":
    main()