# Rollback Procedures

This document outlines the procedures for rolling back the AI-Native Textbook with RAG Chatbot application in case of critical issues in production.

## General Rollback Principles

- Always have a backup plan before deploying
- Ensure backups of data are recent and tested
- Communicate rollback plans with the team
- Document any issues encountered during rollback

## Backend Rollback Procedures

### Railway Rollback
1. **Identify the previous stable version**:
   - Go to the Railway dashboard
   - Navigate to your project and service
   - Check deployment history to find the last stable version

2. **Deploy the previous version**:
   - If using git-based deployment, revert the commit and push
   - If using image-based deployment, select the previous image version

3. **Verify the rollback**:
   - Check that the application is responding correctly
   - Verify key endpoints are working as expected
   - Monitor logs for any errors

### Render Rollback
1. **Access deployment history**:
   - Log in to Render dashboard
   - Go to your web service
   - Navigate to "Manual Deploy" section

2. **Deploy a previous version**:
   - Select a previous commit or build to deploy
   - Initiate the deployment

3. **Monitor the rollback**:
   - Verify the application is responding correctly
   - Check logs for any errors
   - Test critical functionality

### General Backend Rollback
1. **Database considerations**:
   - If database schema changed, have a migration rollback plan
   - Ensure data compatibility with the older version

2. **Environment variables**:
   - Ensure all required environment variables for the previous version are set
   - Remove any new environment variables that the old version doesn't use

3. **Health checks**:
   - Verify health check endpoints are working after rollback
   - Confirm all services are properly connected

## Frontend Rollback Procedures

### GitHub Pages Rollback
1. **Identify the last stable build**:
   - Check GitHub Actions history for the last successful deployment
   - Locate the commit hash associated with the stable version

2. **Deploy the previous version**:
   - If the previous build artifacts are available, upload them manually
   - Otherwise, revert the source code to the previous version and trigger a new build
   - To trigger a build, you can push a commit to the previous state or use GitHub Actions workflow dispatch

3. **Verify the rollback**:
   - Check that the site is loading correctly
   - Verify all links and functionality are working
   - Test that the API connection is functioning

## Service Dependencies Rollback

### Qdrant Vector Database
1. **If schema changes were made**:
   - Have a backup of the vector database from before the deployment
   - In case of issues, restore from backup
   - Ensure the application version matches the database schema version

2. **Version compatibility**:
   - Ensure Qdrant version is compatible with the application version being rolled back to

## Communication Plan

1. **During rollback**:
   - Inform stakeholders about the rollback
   - Provide expected time for completion
   - Keep communication channels open

2. **After rollback**:
   - Confirm with the team that services are operational
   - Inform users if there was downtime
   - Document the reason for rollback and lessons learned

## Quick Actions Checklist

- [ ] Stop any automated deployments during the rollback process
- [ ] Ensure you have access to production environments
- [ ] Have database backups ready before starting the rollback
- [ ] Inform the team about the rollback action
- [ ] Prepare a communication message for users (if needed)
- [ ] Monitor logs and metrics during the process
- [ ] Validate functionality after rollback is complete

## Post-Rollback Actions

1. **Investigation**:
   - Analyze the logs to understand why the rollback was necessary
   - Determine the root cause of the issue

2. **Fix and Test**:
   - Address the issue in a development environment
   - Perform thorough testing before redeployment
   - Include tests that would have caught this issue

3. **Documentation**:
   - Update this document if new rollback procedures are identified
   - Document the incident and resolution for future reference