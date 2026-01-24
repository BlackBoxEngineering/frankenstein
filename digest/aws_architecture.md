# Frankenstein Logic Filter - AWS Architecture

## Overview

Frankenstein is a **Logic Filter** that validates LLM outputs for factual accuracy and logical coherence. It sits between users and AI systems, providing a validation layer where Logic is master.

## Core Concept

```
User → LLM (ChatGPT/Claude/etc) → Frankenstein Filter → Validated Response
                                         ↓
                                   Proof Ledger
```

**Not a replacement AI - a validation layer on top of existing AIs.**

## AWS Architecture

### Production Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CloudFront                          │
│                    (CDN + Edge Caching)                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                            │
│                  (REST API Endpoint)                        │
│                  /validate (POST)                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Lambda Function                          │
│                 (Frankenstein Validator)                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  1. Receive LLM response                            │  │
│  │  2. Extract claims (via Bedrock)                    │  │
│  │  3. Validate each claim                             │  │
│  │  4. Check contradictions                            │  │
│  │  5. Generate proof                                  │  │
│  │  6. Record to ledger                                │  │
│  │  7. Return validation report                        │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌────────┐          ┌─────────┐         ┌──────────┐
    │Bedrock │          │DynamoDB │         │    S3    │
    │(Claude)│          │ Proof   │         │Knowledge │
    │Extract │          │ Ledger  │         │  Cache   │
    └────────┘          └─────────┘         └──────────┘
```

### Components

#### 1. API Gateway
- **Purpose**: REST API endpoint for validation requests
- **Endpoint**: `POST /validate`
- **Input**: `{ "response": "LLM text to validate" }`
- **Output**: `{ "claims": [...], "validations": [...], "proof_id": "..." }`
- **Features**: 
  - Rate limiting
  - API key authentication
  - CORS for browser extension

#### 2. Lambda Function (Frankenstein Core)
- **Runtime**: Python 3.11
- **Memory**: 512MB (adjustable)
- **Timeout**: 30 seconds
- **Layers**: 
  - Frankenstein validation logic
  - boto3 (AWS SDK)
- **Environment Variables**:
  - `BEDROCK_MODEL_ID`: Claude model for claim extraction
  - `DYNAMODB_TABLE`: Proof ledger table name
  - `S3_BUCKET`: Knowledge cache bucket

#### 3. Amazon Bedrock
- **Model**: Claude 3 Haiku (fast, cheap) or Sonnet (better reasoning)
- **Purpose**: Extract factual claims from LLM responses
- **Prompt**: "Extract all factual claims from this text..."
- **Cost**: ~$0.00025 per request (Haiku)

#### 4. DynamoDB (Proof Ledger)
- **Table**: `frankenstein-proof-ledger`
- **Primary Key**: `proof_id` (UUID)
- **Sort Key**: `timestamp`
- **Attributes**:
  - `claims`: List of claims validated
  - `validations`: Results for each claim
  - `hash`: Cryptographic hash
  - `prev_hash`: Previous record hash (chain)
- **Features**:
  - Point-in-time recovery
  - Encryption at rest
  - Global secondary index on timestamp

#### 5. S3 (Knowledge Cache)
- **Bucket**: `frankenstein-knowledge-cache`
- **Purpose**: Cache Wikipedia/Wikidata lookups
- **Structure**:
  ```
  /facts/
    /entity_123.json
    /relation_456.json
  /rules/
    /taxonomy.json
    /inference_rules.json
  ```
- **Lifecycle**: 30-day expiration for cached facts

#### 6. CloudFront (Optional)
- **Purpose**: CDN for API responses
- **Benefits**: 
  - Lower latency globally
  - Reduced Lambda invocations
  - Caching for common validations

### Data Flow

```
1. User submits LLM response
   ↓
2. API Gateway receives request
   ↓
3. Lambda invoked
   ↓
4. Bedrock extracts claims
   "Cats are mammals that live underwater"
   → ["Cats are mammals", "Cats live underwater"]
   ↓
5. For each claim:
   a. Check S3 cache
   b. If not cached, lookup Wikipedia/Wikidata
   c. Run inference engine
   d. Check contradictions
   e. Generate validation result
   ↓
6. Create proof record
   - Hash all validations
   - Link to previous record
   - Store in DynamoDB
   ↓
7. Return validation report
   {
     "claims": [
       {"text": "Cats are mammals", "valid": true, "confidence": 1.0},
       {"text": "Cats live underwater", "valid": false, "proof": "..."}
     ],
     "proof_id": "uuid-123",
     "timestamp": "2024-01-15T10:30:00Z"
   }
```

## Local Development Architecture

```
Local Machine
    ↓
FastAPI (localhost:8000)
    ↓
├─ Frankenstein Core (Python)
├─ Local DynamoDB (Docker)
└─ Mock Bedrock (hardcoded extraction)
```

**Development Flow:**
1. Build validation logic locally
2. Test with FastAPI
3. Use DynamoDB Local (Docker)
4. Mock Bedrock responses
5. Once working, deploy to AWS

## Deployment Strategy

### Phase 1: Local Development
- FastAPI application
- SQLite for proof ledger (simple)
- Hardcoded claim extraction
- Test validation logic

### Phase 2: AWS Deployment
- Package Lambda function
- Deploy with SAM/CDK
- Connect DynamoDB
- Add Bedrock integration

### Phase 3: Frontend
- Web UI (Amplify)
- Browser extension
- API documentation

## Infrastructure as Code

### SAM Template (template.yaml)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  FrankensteinAPI:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.11
      Handler: app.validate
      MemorySize: 512
      Timeout: 30
      Environment:
        Variables:
          DYNAMODB_TABLE: !Ref ProofLedger
          S3_BUCKET: !Ref KnowledgeCache
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref ProofLedger
        - S3CrudPolicy:
            BucketName: !Ref KnowledgeCache
        - Statement:
            - Effect: Allow
              Action: bedrock:InvokeModel
              Resource: '*'
      Events:
        Validate:
          Type: Api
          Properties:
            Path: /validate
            Method: post

  ProofLedger:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: frankenstein-proof-ledger
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: proof_id
          AttributeType: S
        - AttributeName: timestamp
          AttributeType: S
      KeySchema:
        - AttributeName: proof_id
          KeyType: HASH
        - AttributeName: timestamp
          KeyType: RANGE

  KnowledgeCache:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: frankenstein-knowledge-cache
      LifecycleConfiguration:
        Rules:
          - ExpirationInDays: 30
            Status: Enabled
```

## Security

### Authentication
- API Gateway API keys
- IAM roles for Lambda
- S3 bucket policies

### Data Protection
- DynamoDB encryption at rest
- S3 encryption
- TLS for all API calls

### Audit Trail
- CloudWatch Logs for all Lambda invocations
- DynamoDB proof ledger (immutable)
- X-Ray tracing for debugging

## Cost Optimization

### Free Tier Usage
- Lambda: 1M requests/month free
- DynamoDB: 25GB storage free
- S3: 5GB storage free
- API Gateway: 1M requests/month free

### Estimated Costs (After Free Tier)
- **1,000 validations/day**: ~$3/month
- **10,000 validations/day**: ~$30/month
- **100,000 validations/day**: ~$300/month

**Breakdown:**
- Lambda: $0.20 per 1M requests
- Bedrock: $0.25 per 1M tokens (Haiku)
- DynamoDB: $1.25 per 1M writes
- S3: $0.023 per GB

## Monitoring

### CloudWatch Metrics
- Lambda invocations
- Error rates
- Latency (p50, p99)
- DynamoDB read/write capacity

### Alarms
- Error rate > 5%
- Latency > 5 seconds
- DynamoDB throttling

### Dashboards
- Real-time validation stats
- Proof ledger integrity
- Cache hit rates

## Scalability

### Current Limits
- Lambda: 1,000 concurrent executions
- DynamoDB: Unlimited (on-demand)
- API Gateway: 10,000 requests/second

### Scaling Strategy
- Lambda auto-scales
- DynamoDB on-demand billing
- CloudFront caching for common validations
- S3 knowledge cache reduces external API calls

## Next Steps

1. **Document complete** ✓
2. **Build locally** (Phase 1)
   - FastAPI validation service
   - SQLite proof ledger
   - Test validation logic
3. **Deploy to AWS** (Phase 2)
   - SAM deployment
   - DynamoDB integration
   - Bedrock integration
4. **Build frontend** (Phase 3)
   - Web UI
   - Browser extension

---

**This architecture provides:**
- Scalable validation service
- Immutable audit trail
- Cost-effective operation
- Easy deployment
- Production-ready infrastructure
