# Blockchain Bootcamp Backend

Backend API untuk aplikasi bootcamp berbasis blockchain yang menggunakan FastAPI dan Ethereum untuk menerbitkan sertifikat terverifikasi.

## 🏗️ Struktur Project

```
blockchain-bootcamp-backend/
├── alembic/                    # Database migrations
│   ├── versions/
│   │   └── 001_initial_migration.py
│   └── env.py
├── app/
│   ├── config/                 # Konfigurasi aplikasi
│   │   ├── settings.py         # Environment settings
│   │   └── blockchain.py       # Blockchain configuration
│   ├── db/                     # Database session
│   │   └── session.py
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── course.py
│   │   ├── chapter.py
│   │   ├── user_progress.py
│   │   ├── quiz_answer.py
│   │   └── certificate.py
│   ├── repositories/           # Data access layer
│   │   ├── user_repository.py
│   │   ├── course_repository.py
│   │   ├── chapter_repository.py
│   │   ├── progress_repository.py
│   │   ├── quiz_repository.py
│   │   └── certificate_repository.py
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   ├── course_service.py
│   │   ├── chapter_service.py
│   │   ├── quiz_service.py
│   │   ├── certificate_service.py
│   │   └── blockchain_service.py
│   ├── controllers/            # Request handlers
│   │   ├── auth_controller.py
│   │   ├── course_controller.py
│   │   ├── chapter_controller.py
│   │   ├── quiz_controller.py
│   │   └── certificate_controller.py
│   ├── routes/                 # API routes
│   │   └── api_v1.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user_schema.py
│   │   ├── course_schema.py
│   │   ├── chapter_schema.py
│   │   ├── quiz_schema.py
│   │   └── certificate_schema.py
│   ├── helpers/                # Utility functions
│   │   ├── password_helper.py
│   │   ├── jwt_helper.py
│   │   └── blockchain_helper.py
│   └── main.py                 # FastAPI app entry point
├── contracts/                  # Smart contracts
│   ├── CertificateRegistry.sol
│   ├── build/                  # Compiled contracts
│   ├── compile_contract.sh     # Compilation script
│   └── deploy_contract.py      # Deployment script
├── scripts/
│   └── seed_courses.py         # Seed database with courses
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 13+
- Geth (Go Ethereum)
- Solidity Compiler (solc)
- Docker (opsional, untuk PostgreSQL)

### 1. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Environment Variables

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env dan isi konfigurasi
nano .env
```

**Penting**: Isi semua variable kecuali `CONTRACT_ADDRESS` (akan diisi setelah deploy contract)

### 3. Start Blockchain Network

#### Terminal 1: Bootnode

```bash
cd local-eth-net/bootnode
bootnode -nodekey boot.key -addr :30310
```

#### Terminal 2: Signer Node

```bash
export BOOTNODE_ENODE="enode://25ab14af6e485ab27f6ed4d9cea1795bc99235b25d82ea610dc5a5f7bd76eb12ec86f27f49c7fdfa9ff7dc6c5cd90c02287f3a17fe612d55d20946531917136d@127.0.0.1:0?discport=30310"

geth --datadir ./local-eth-net/nodes/node-signer \
--networkid 110261 \
--bootnodes $BOOTNODE_ENODE \
--http --http.addr 0.0.0.0 --http.port 8545 --http.api eth,net,web3,personal,admin,clique \
--port 30303 \
--authrpc.port 8551 \
--mine \
--miner.etherbase 0xC58BD29d19B38Bc00a9Fa108971637D050fbd57C \
--unlock 0xC58BD29d19B38Bc00a9Fa108971637D050fbd57C \
--password ./local-eth-net/nodes/node-signer/password.txt \
--allow-insecure-unlock \
--rpc.enabledeprecatedpersonal
```

### 4. Setup PostgreSQL Database

```bash
# Menggunakan Docker
docker run -d \
--name blockchain-bootcamp-db \
-e POSTGRES_DB=bootcamp \
-e POSTGRES_USER=user \
-e POSTGRES_PASSWORD=rayhankaya123 \
-p 5432:5432 \
postgres:13

# Atau install PostgreSQL langsung dan buat database
createdb bootcamp
```

### 5. Compile Smart Contract

```bash
# Make script executable
chmod +x contracts/compile_contract.sh

# Compile contract
./contracts/compile_contract.sh
```

### 6. Deploy Smart Contract

```bash
python contracts/deploy_contract.py
```

**⚠️ PENTING**: Setelah deployment, copy `CONTRACT_ADDRESS` yang muncul ke file `.env`

```env
CONTRACT_ADDRESS=0xYourContractAddressHere
```

### 7. Run Database Migrations

```bash
# Run migrations
alembic upgrade head
```

### 8. Seed Database

```bash
# Seed courses and chapters
python scripts/seed_courses.py
```

### 9. Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API akan berjalan di `http://localhost:8000`

Dokumentasi API (Swagger): `http://localhost:8000/docs`

## 📡 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register user baru
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get user profile (protected)

### Courses

- `GET /api/v1/courses` - Get semua courses (protected)
- `GET /api/v1/courses/{course_id}` - Get detail course (protected)

### Chapters

- `GET /api/v1/chapters/course/{course_id}` - Get chapters by course (protected)
- `GET /api/v1/chapters/{chapter_id}` - Get chapter detail (protected)

### Quiz

- `POST /api/v1/quiz/submit` - Submit quiz answer (protected)

### Certificates

- `POST /api/v1/certificates/claim` - Claim certificate (protected)
- `GET /api/v1/certificates/my-certificates` - Get user certificates (protected)
- `POST /api/v1/certificates/verify` - Verify certificate (public)

## 🔐 Authentication

API menggunakan JWT Bearer Token. Setelah login, gunakan token dalam header:

```
Authorization: Bearer <your_token_here>
```

## 💾 Database Schema

### Tables

- **users** - User accounts
- **courses** - Available courses
- **chapters** - Course chapters with content and quiz
- **user_progress** - User progress per course
- **quiz_answers** - User quiz submissions
- **certificates** - Issued certificates with blockchain verification

## 🔗 Blockchain Integration

### Smart Contract

Contract `CertificateRegistry.sol` menyimpan hash certificate untuk verifikasi.

**Key Functions**:
- `storeCertificate(certificateId, certificateHash)` - Store certificate hash
- `verifyHash(certificateId, certificateHash)` - Verify certificate
- `getTimestamp(certificateId)` - Get certificate timestamp

### Certificate Process

1. User menyelesaikan minimal 2 chapters
2. User klaim certificate
3. Backend generate certificate data dan hash
4. Hash disimpan ke blockchain via smart contract
5. Certificate metadata disimpan di PostgreSQL
6. Blockchain transaction hash dan block number di-record

## 🧪 Testing Flow

### 1. Register & Login

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
-H "Content-Type: application/json" \
-d '{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email": "test@example.com",
  "password": "password123"
}'
```

### 2. Get Courses

```bash
curl -X GET http://localhost:8000/api/v1/courses \
-H "Authorization: Bearer <your_token>"
```

### 3. Get Chapter & Submit Quiz

```bash
# Get chapter
curl -X GET http://localhost:8000/api/v1/chapters/1 \
-H "Authorization: Bearer <your_token>"

# Submit quiz answer
curl -X POST http://localhost:8000/api/v1/quiz/submit \
-H "Authorization: Bearer <your_token>" \
-H "Content-Type: application/json" \
-d '{
  "chapter_id": 1,
  "answer_index": 2
}'
```

### 4. Claim Certificate

```bash
curl -X POST http://localhost:8000/api/v1/certificates/claim \
-H "Authorization: Bearer <your_token>" \
-H "Content-Type: application/json" \
-d '{
  "course_id": 1
}'
```

### 5. Verify Certificate

```bash
curl -X POST http://localhost:8000/api/v1/certificates/verify \
-H "Content-Type: application/json" \
-d '{
  "certificate_id": "CERT-1-1-20251110120000"
}'
```

## 🛠️ Development Tips

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Upgrade to latest
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Show current version
alembic current
```

### Check Blockchain Connection

```bash
# Attach to geth console
geth attach http://127.0.0.1:8545

# Check accounts
> eth.accounts

# Check balance
> eth.getBalance(eth.accounts[0])

# Check latest block
> eth.blockNumber
```

### Reset Database

```bash
# Drop all tables
alembic downgrade base

# Recreate tables
alembic upgrade head

# Reseed data
python scripts/seed_courses.py
```

## 📝 Notes

- Ini adalah development setup untuk tugas blockchain, bukan production-ready
- Blockchain berjalan di local network dengan PoA (Clique)
- Hanya menggunakan 2 nodes: bootnode dan signer-node
- JWT digunakan untuk auth, CORS enabled untuk frontend
- Certificate hash di-blockchain-kan untuk verifikasi integritas

## 🐛 Troubleshooting

### Blockchain tidak connect

```bash
# Check if geth is running
ps aux | grep geth

# Check RPC connection
curl -X POST http://localhost:8545 \
-H "Content-Type: application/json" \
-d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### Database connection error

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check connection
psql -U user -d bootcamp -h localhost
```

### Smart contract not deployed

```bash
# Recompile
./contracts/compile_contract.sh

# Redeploy
python contracts/deploy_contract.py

# Update .env with new CONTRACT_ADDRESS
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Solidity Documentation](https://docs.soliditylang.org/)
- [Geth Documentation](https://geth.ethereum.org/docs)

## 👨‍💻 Author

Developed for Blockchain Development Course Assignment