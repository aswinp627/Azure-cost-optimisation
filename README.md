
# 💰 Azure Cost Optimization – Serverless Billing Records

This project presents a **cost optimization solution** for managing billing records in a serverless Azure architecture using **Cosmos DB** and **Azure Blob Storage**.

---

## 📌 Problem Statement

- **High Cost**: Over 2 million records in Azure Cosmos DB are increasing storage and RU/s costs.
- **Access Pattern**: Most reads are for recent data. Older data (3+ months) is rarely accessed.
- **Constraints**:
  - No API changes
  - No downtime or data loss
  - Simple to implement and maintain

---

## ✅ Solution Overview

1. **Recent data (last 3 months)** stays in Cosmos DB.
2. **Older data** is archived into **Azure Blob Storage** (Cool/Archive tier).
3. A fallback Azure Function checks Blob if Cosmos DB does not have the record.

```

---

## ⚙️ How It Works

### 1. Archiving Old Records
- A scheduled Python script (`archive_old_data.py`) runs daily/weekly:
  - Moves billing records older than 3 months from Cosmos DB to Blob.
  - Saves them as compressed `.json.gz` files in folders like `2023/05/records.json.gz`.

### 2. Reading Records
- Azure Function (`read_fallback_function.js`) acts as a read handler:
  - Tries to fetch record from Cosmos DB.
  - If not found, reads the appropriate Blob file, decompresses, and returns the record.

---

## 🚀 Benefits

| Feature            | Benefit                           |
|--------------------|------------------------------------|
| Serverless & Simple| Easy to deploy, manage, and scale  |
| Cost-Efficient     | Blob Storage is 90% cheaper        |
| No Contract Change | APIs remain exactly the same       |
| No Downtime        | All transitions happen in background|

---


## 🤖 AI-Generated Help

See [chatgpt-session.md](./chatgpt-session.md) for the conversation used to build this project.
