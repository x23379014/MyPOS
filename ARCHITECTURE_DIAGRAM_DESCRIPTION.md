# Architecture Diagram Description for AI Image Generation

## Visual Description for AI Image Generator

Create a clean, professional architecture diagram showing a cloud-based Point of Sale system with the following layout and components:

### Overall Layout
- **Top to Bottom Flow**: Diagram should flow from top (users) to bottom (data storage)
- **Color Scheme**: Use blue tones for AWS services, green for data storage, orange/yellow for compute
- **Style**: Modern, clean, professional - similar to AWS architecture diagrams

### Components and Their Visual Representation

#### 1. Top Layer - Users (Top Center)
- **Icon/Shape**: Multiple user icons or a cloud symbol representing internet users
- **Label**: "Users" or "Internet Users"
- **Color**: Light gray or blue
- **Position**: Centered at the top

#### 2. Application Load Balancer (Below Users, Centered)
- **Shape**: Horizontal rectangle or rounded rectangle
- **Label**: "Application Load Balancer (ALB)"
- **Sub-labels**: 
  - "Routes Traffic"
  - "Health Checks"
- **Color**: Blue (AWS service color)
- **Icon**: Optional load balancer icon
- **Position**: Centered, below users

#### 3. EC2 Instances (Below ALB, Side by Side)
- **Two identical boxes** placed horizontally next to each other
- **Shape**: Rectangles or server icons
- **Labels**: 
  - Left box: "EC2 Instance 1" and "Django App"
  - Right box: "EC2 Instance 2" and "Django App"
- **Color**: Orange or light blue
- **Icons**: Server/computer icons
- **Position**: Below ALB, horizontally aligned

#### 4. AWS Services (Bottom Layer, Five Boxes in a Row)
Five service boxes arranged horizontally:

**a) DynamoDB (Leftmost)**
- **Shape**: Database icon or rounded rectangle
- **Label**: "DynamoDB"
- **Sub-labels**: 
  - "Customers"
  - "Transactions"
- **Color**: Blue (AWS service)
- **Icon**: Database symbol

**b) Amazon S3 (Second from left)**
- **Shape**: Storage bucket icon or rectangle
- **Label**: "Amazon S3"
- **Sub-labels**: 
  - "Product Images"
- **Color**: Blue (AWS service)
- **Icon**: Storage/bucket symbol

**c) Amazon SNS (Center)**
- **Shape**: Notification/bell icon or rectangle
- **Label**: "Amazon SNS"
- **Sub-labels**: 
  - "Notifications"
- **Color**: Blue (AWS service)
- **Icon**: Notification/bell symbol

**d) CloudWatch (Second from right)**
- **Shape**: Monitoring/eye icon or rectangle
- **Label**: "CloudWatch"
- **Sub-labels**: 
  - "Metrics"
  - "Logs"
- **Color**: Blue (AWS service)
- **Icon**: Monitoring/eye symbol

**e) SQLite (Rightmost)**
- **Shape**: Database icon or rectangle
- **Label**: "SQLite"
- **Sub-labels**: 
  - "Products"
- **Color**: Green or gray (local database)
- **Icon**: Database symbol

### Connection Lines (Arrows)

1. **From Users to ALB**: 
   - Downward arrow
   - Label: "HTTP Requests"
   - Color: Black or dark gray

2. **From ALB to EC2 Instances**:
   - Two downward arrows branching from ALB
   - One arrow to each EC2 instance
   - Color: Black or dark gray

3. **From EC2 Instances to AWS Services**:
   - Five arrows from each EC2 instance (or from a common point below EC2)
   - Arrows pointing down to each of the five services
   - Color: Black or dark gray
   - Can show as: EC2 → (common point) → Services

### Text Annotations

Add small text labels near arrows or components:
- "HTTP Requests" near the user-to-ALB arrow
- "Data Storage" near the services layer
- Optional: "Cloud Services" label above AWS services

### Visual Style Guidelines

- **Background**: White or light gray
- **Boxes**: Rounded corners, subtle shadows
- **Text**: Clear, readable fonts (Arial, Helvetica, or similar)
- **Arrows**: Solid lines with arrowheads
- **Spacing**: Adequate spacing between components
- **Alignment**: Components should be well-aligned
- **Icons**: Use recognizable icons for each service type

### Alternative Layout Description

If horizontal layout doesn't work, use this vertical description:

**Left to Right Flow:**
1. **Left**: Users icon
2. **Center-Left**: ALB box
3. **Center**: Two EC2 boxes stacked or side-by-side
4. **Right**: Five AWS service boxes arranged vertically or in a grid

### Key Visual Elements to Emphasize

1. **Flow Direction**: Clear top-to-bottom or left-to-right flow
2. **Service Grouping**: AWS services should be visually grouped together
3. **Connection Clarity**: All connections should be clearly visible
4. **Labels**: All components should have clear labels
5. **Color Coding**: Use consistent colors for similar component types

### Sample Prompt for AI Image Generator

"Create a professional cloud architecture diagram showing:
- Top: Users/internet icon
- Below: Application Load Balancer (blue box)
- Below that: Two EC2 instances side by side (orange boxes labeled Django App)
- Bottom: Five AWS service boxes in a row - DynamoDB (customers/transactions), S3 (product images), SNS (notifications), CloudWatch (metrics/logs), and SQLite (products)
- Arrows showing data flow from users down through ALB to EC2 instances, then down to the AWS services
- Clean, modern style similar to AWS architecture diagrams with blue for AWS services, orange for compute, and clear labels on all components"

---

## Detailed Component Descriptions

### Users Component
- **Visual**: Cloud icon with multiple user silhouettes, or simple "Users" text box
- **Color**: Light blue or gray
- **Size**: Medium, centered at top

### Application Load Balancer
- **Visual**: Horizontal rectangle with rounded corners
- **Color**: AWS blue (#FF9900 or standard AWS blue)
- **Text**: Bold "Application Load Balancer" at top, smaller sub-text below
- **Size**: Wider than it is tall

### EC2 Instances
- **Visual**: Two identical server/computer icons or boxes
- **Color**: Orange (#FF9900) or light blue
- **Text**: "EC2 Instance 1/2" and "Django App"
- **Size**: Medium, equal size, side by side

### AWS Services Row
- **Visual**: Five equal-sized boxes/icons in a horizontal row
- **Spacing**: Equal spacing between boxes
- **Alignment**: All boxes aligned at the same height
- **Icons**: Each service should have its recognizable icon
  - DynamoDB: Database icon
  - S3: Storage bucket icon
  - SNS: Notification/bell icon
  - CloudWatch: Eye/monitoring icon
  - SQLite: Database icon (different from DynamoDB)

### Connection Lines
- **Style**: Solid lines with arrowheads
- **Thickness**: Medium (2-3px)
- **Color**: Dark gray or black
- **Direction**: All arrows point downward (or right if horizontal layout)

---

This description should help generate an accurate visual representation of the MyPOS architecture!

