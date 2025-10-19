# Friction Log – AI Operations Command Center 2.0

This document summarizes the key challenges we faced while building AOCC 2.0 during the Agents in Production Hackathon, along with the approaches we used to resolve them.  
The intent is to provide constructive feedback for improving future developer experiences with agentic workflows.

---

## 1. Environment Setup on Windows
**Issue:**  
Setting up the Python virtual environment was inconsistent on Windows.  
- `py -m venv .venv` was not recognized.  
- Activating `.venv\Scripts\Activate.ps1` sometimes failed due to OneDrive folder permissions.  

**Resolution:**  
We standardized on:  
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
