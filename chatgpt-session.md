# ChatGPT Session Summary – Azure Cost Optimization Project
 
**Candidate**: Aswin P  
**Reviewed by**: ChatGPT (GPT-4o)  
**Date**: 2025-08-07  
**Context**: Azure Serverless Cost Optimization – Cosmos DB archival with Blob Storage fallback
 
---
 
## 🔍 Problem Summary
 
The candidate needed to reduce **Cosmos DB costs** in a **read-heavy Azure serverless architecture** where:
- Billing records up to **300 KB** each
- Over **2 million records**
- Records older than 3 months are rarely accessed
- Data must always be available via **unchanged APIs**, with **low latency** for old records
 
---
 
## ✅ Proposed Solution (with ChatGPT Assistance)
 
### Architecture Overview
- Hot data (≤3 months): Stored in **Cosmos DB**
- Cold data (>3 months): Moved to **Azure Blob Storage** (archived monthly)
- A fallback **Azure Function** reads from Blob if Cosmos misses
- Archive process is **automated, incremental, and safe**
 
---
 
## 🛠 Key Components Generated
 
### 1. **Architecture Diagram**
Explains how billing records flow through Cosmos DB, Blob, and fallback reader.  
[✓ architecture.png]
 
---
 
### 2. **Archival Script**
**File**: `scripts/archive_old_data.py`  
- Connects to Cosmos DB
- Filters records older than 3 months
- Compresses and uploads them to Blob Storage
- Deletes safely from Cosmos after verification
 
---
 
### 3. **Fallback Reader Function**
**File**: `scripts/read_fallback_function.js`  
- First checks Cosmos DB for the record
- If missing, reads from archived `.json.gz` in Blob
- Transparent to API consumers
 
---
 
### 4. **README.md File**
Summarizes:
- Problem
- Solution design
- Architecture and fallback strategy
- Scripts involved
- Deployment/operational simplicity
 
---
 
## 🎯 Constraints Satisfied
 
| Requirement                        | Met | Notes |
|-----------------------------------|-----|-------|
| Simplicity & Ease of Deployment   | ✅  | Straightforward Azure Function & script |
| No Downtime or Data Loss          | ✅  | Uses staged archival and backup logic |
| No API Contract Changes           | ✅  | Reader handles routing logic |
| Cold Data Response Time (Seconds) | ✅  | Fetch from Blob within acceptable latency |
 
---
 
## 💡 Bonus Considerations Discussed
 
- Fallback logic handles decompression & parsing for large blobs
- Indexing strategies for large archive files discussed
- Cosmos TTL and change feed evaluated but not chosen (cost/simplicity trade-off)
- Retention logic and fail-safes built into script
