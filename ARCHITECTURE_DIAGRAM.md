# MyPOS - System Architecture Diagram

## System Architecture

```
                    ┌──────────────┐
                    │    Users     │
                    │  (Browsers)  │
                    └──────┬───────┘
                           │
                           │ HTTP Requests
                           ▼
        ┌──────────────────────────────────┐
        │  Application Load Balancer (ALB) │
        │  - Routes traffic                 │
        │  - Health checks                  │
        └──────────────┬───────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
    ┌──────────┐             ┌──────────┐
    │ EC2-1    │             │ EC2-2    │
    │ Django   │             │ Django   │
    │ App      │             │ App      │
    └────┬─────┘             └────┬─────┘
         │                        │
         └───────────┬────────────┘
                     │
         ┌───────────┼───────────┬───────────┬───────────┐
         │           │           │           │           │
         ▼           ▼           ▼           ▼           ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │DynamoDB │ │   S3    │ │   SNS   │ │CloudWatch│ │ SQLite │
    │         │ │         │ │         │ │         │ │         │
    │Customers│ │ Product │ │ Notif-  │ │ Metrics │ │Products │
    │Transact │ │ Images  │ │ ications│ │  Logs   │ │  Data   │
    └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

## Data Flow

**Where Data Goes:**

1. **Customer Data** → DynamoDB (Customers Table)
2. **Transaction Data** → DynamoDB (Transactions Table)
3. **Product Images** → S3 Bucket
4. **Product Data** → SQLite Database (Local)
5. **Transaction Notifications** → SNS Topic
6. **System Metrics** → CloudWatch

## Services Used

| Service | Purpose | Data Stored |
|---------|---------|------------|
| **Application Load Balancer (ALB)** | Distributes traffic to EC2 instances | None (Routing only) |
| **EC2 Instances** | Run Django application | Application code |
| **DynamoDB** | NoSQL database | Customers, Transactions |
| **Amazon S3** | Object storage | Product images |
| **Amazon SNS** | Notification service | Notification messages |
| **CloudWatch** | Monitoring service | Metrics, Logs |
| **SQLite** | Local database | Products (local) |

## Request Flow

```
User Request
    │
    ▼
Application Load Balancer
    │
    ▼
EC2 Instance (Django)
    │
    ├──► Customer CRUD ──► DynamoDB
    ├──► Transaction ──► DynamoDB ──► SNS ──► CloudWatch
    ├──► Product Image ──► S3
    └──► Product CRUD ──► SQLite
```

## Architecture Summary

- **Frontend**: HTML/CSS (Templates)
- **Backend**: Django Application (Python)
- **Load Balancing**: Application Load Balancer
- **Compute**: EC2 Instances (Amazon Linux 2)
- **Database**: DynamoDB (Cloud) + SQLite (Local)
- **Storage**: S3 (Images)
- **Notifications**: SNS
- **Monitoring**: CloudWatch

---

## AI Image Generation Prompt

**Copy this prompt to generate the architecture diagram image:**

```
Create a professional cloud architecture diagram with a vertical top-to-bottom flow:

TOP LAYER:
- Centered at top: "Users" icon/box (light blue/gray) representing internet users/browsers

MIDDLE LAYER:
- Below users: "Application Load Balancer (ALB)" horizontal rectangle (AWS blue color)
  - Sub-text: "Routes traffic" and "Health checks"
- Below ALB: Two identical boxes side by side labeled "EC2 Instance 1" and "EC2 Instance 2" (orange/light blue)
  - Each box contains: "Django App" text
  - Both boxes are the same size and horizontally aligned

BOTTOM LAYER:
- Below EC2 instances: Five service boxes arranged horizontally in a row:
  1. "DynamoDB" (AWS blue) - sub-text: "Customers" and "Transactions"
  2. "Amazon S3" (AWS blue) - sub-text: "Product Images"
  3. "Amazon SNS" (AWS blue) - sub-text: "Notifications"
  4. "CloudWatch" (AWS blue) - sub-text: "Metrics" and "Logs"
  5. "SQLite" (green/gray) - sub-text: "Products"

CONNECTIONS:
- Downward arrow from Users to ALB labeled "HTTP Requests"
- Two downward arrows from ALB branching to each EC2 instance
- Five downward arrows from EC2 instances (or from a common point below them) connecting to each of the five services

STYLE:
- Clean, modern AWS-style architecture diagram
- White or light gray background
- Rounded corners on boxes
- Clear labels on all components
- Professional color scheme: AWS blue for AWS services, orange for compute, green/gray for local database
- All components well-aligned and evenly spaced
```

**Alternative shorter prompt:**

```
Create a cloud architecture diagram showing: Users at top → Application Load Balancer (blue box) → Two EC2 instances side by side (orange boxes with "Django App") → Five AWS services in a row at bottom: DynamoDB (customers/transactions), S3 (product images), SNS (notifications), CloudWatch (metrics/logs), and SQLite (products). Use downward arrows showing data flow. AWS-style professional diagram with blue for AWS services, orange for compute.
```
