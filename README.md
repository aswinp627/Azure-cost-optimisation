# Azure-cost-optimisation
🔧 Goal
Reduce Cosmos DB costs by moving older billing records (older than 3 months) to cheaper storage, while still allowing users to access them without breaking the current APIs.
✅ Simple Strategy
1. Keep recent records in Cosmos DB
Only keep the last 3 months of billing records in Cosmos DB.
These are frequently accessed, so performance is critical.
2. Move older records to Azure Blob Storage
Billing records older than 3 months are moved to Azure Blob Storage, which is much cheaper than Cosmos DB.
Data is stored as compressed JSON files, organized by month or year.
3. Read from Cosmos DB first, Blob second
When someone requests a record:
First, check Cosmos DB.
If the record is not found, check Azure Blob Storage.
This way, your existing APIs continue to work without any changes.
🧱 Simple Architecture Diagram
pgsqlCopyEdit                    ┌───────────────────────┐
                    │    API / Frontend     │
                    └────────┬──────────────┘
                             │
                  ┌──────────▼─────────┐
                  │  Azure Function    │
                  │  (Read handler)    │
                  └─────┬──────────────┘
                        │
      ┌─────────────────▼─────────────┐
      │     Azure Cosmos DB (hot)     │◄── Last 3 months of data
      └─────────────────┬─────────────┘
                        │ (if not found)
                        ▼
         ┌────────────────────────────┐
         │ Azure Blob Storage (cold)  │◄── Archived old records
         └────────────────────────────┘
🛠️ How Archival Works
You can create a scheduled function (once a day/week) that does the following:
Query Cosmos DB for records older than 3 months.
Save them as a .json.gz file to Blob Storage.
Delete those records from Cosmos DB.
Here’s some pseudocode:
pythonCopyEdit# Archive old records to blobrecords = query_cosmosdb("older than 3 months")
for record in records:
    save_to_blob("YYYY-MM/record.json.gz", record)
delete_from_cosmosdb(records)
🧪 How Reads Work (Pseudocode)
pythonCopyEditdef get_billing_record(record_id):
    record = get_from_cosmos(record_id)
    if record:
        return record
    
    record = get_from_blob(record_id)  # search in blob storagereturn record or "Record not found" 
You can run this as an Azure Function, and call it from your API.
✅ Why This Works
Requirement	Solution
No API changes	Existing API calls Azure Function which handles fallback
No downtime	Runs in background, no impact to users
No data loss	Data is copied to blob before deleting from Cosmos DB
Simple to implement	Uses built-in Azure tools: Functions, Blob, TTL, Scheduler
Cost savings	Blob Storage is 90%+ cheaper for archived data
 
🛡️ Problems You Might Face
 
Problem	Fix
Blob files get too big	Split by month or by 1000 records
Slow read from Blob	Pre-load recent archives in memory or add small cache
Record not found in both	Add monitoring to alert if archival step failed
 
