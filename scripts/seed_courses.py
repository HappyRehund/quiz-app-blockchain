# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# from sqlalchemy.orm import Session
# from app.db.session import engine, SessionLocal
# from app.models.course import Course
# from app.models.chapter import Chapter
# import json

# def seed_courses():
#     db = SessionLocal()
    
#     try:
#         # Check if courses already exist
#         existing_courses = db.query(Course).count()
#         if existing_courses > 0:
#             print(f"⚠️  Database already has {existing_courses} course(s). Skipping seed.")
#             return
        
#         # Course 1: Introduction to Blockchain
#         course1 = Course(
#             title="Introduction to Blockchain Technology",
#             description="Learn the fundamentals of blockchain technology, including its history, core concepts, and real-world applications."
#         )
#         db.add(course1)
#         db.flush()
        
#         # Course 1 Chapters
#         chapters_course1 = [
#             {
#                 "chapter_number": 1,
#                 "title": "What is Blockchain?",
#                 "content": """Blockchain is a distributed ledger technology that maintains a continuously growing list of records called blocks. Each block contains a cryptographic hash of the previous block, a timestamp, and transaction data. This structure makes the blockchain resistant to modification of data.

# The key characteristics of blockchain include:
# - Decentralization: No central authority controls the blockchain
# - Transparency: All transactions are visible to network participants
# - Immutability: Once recorded, data cannot be easily altered
# - Security: Cryptographic techniques protect the data

# Blockchain was first conceptualized in 2008 by an individual or group known as Satoshi Nakamoto as the foundation for Bitcoin cryptocurrency.""",
#                 "quiz_question": "Which of the following is NOT a key characteristic of blockchain?",
#                 "quiz_options": ["Decentralization", "Transparency", "Centralized Control", "Immutability"],
#                 "quiz_correct_answer": 2
#             },
#             {
#                 "chapter_number": 2,
#                 "title": "How Blockchain Works",
#                 "content": """Blockchain works through a process of recording transactions in blocks that are linked together in a chain. Here's how it works:

# 1. Transaction Initiation: A user requests a transaction
# 2. Broadcasting: The transaction is broadcast to all nodes in the network
# 3. Validation: Network nodes validate the transaction using consensus mechanisms
# 4. Block Creation: Validated transactions are combined into a new block
# 5. Hashing: The new block is given a unique hash
# 6. Addition to Chain: The block is added to the blockchain
# 7. Transaction Complete: The transaction is complete and recorded permanently

# The consensus mechanism ensures all nodes agree on the blockchain's state. Popular mechanisms include Proof of Work (PoW) and Proof of Stake (PoS).""",
#                 "quiz_question": "What is the purpose of a consensus mechanism in blockchain?",
#                 "quiz_options": ["To slow down transactions", "To ensure all nodes agree on the blockchain's state", "To delete old blocks", "To create new cryptocurrencies"],
#                 "quiz_correct_answer": 1
#             },
#             {
#                 "chapter_number": 3,
#                 "title": "Types of Blockchain",
#                 "content": """There are three main types of blockchain networks:

# 1. Public Blockchain: Open to anyone, fully decentralized, and transparent. Examples include Bitcoin and Ethereum. Anyone can join, participate, and view all transactions.

# 2. Private Blockchain: Restricted access, controlled by a single organization. Suitable for internal business processes where privacy is important. Faster than public blockchains but less decentralized.

# 3. Consortium Blockchain: Semi-decentralized, controlled by a group of organizations. Combines benefits of both public and private blockchains. Used in industries where multiple organizations need to collaborate.

# Each type has its own use cases and trade-offs between decentralization, privacy, and performance.""",
#                 "quiz_question": "Which blockchain type is open to anyone and fully decentralized?",
#                 "quiz_options": ["Private Blockchain", "Consortium Blockchain", "Public Blockchain", "Hybrid Blockchain"],
#                 "quiz_correct_answer": 2
#             },
#             {
#                 "chapter_number": 4,
#                 "title": "Blockchain Applications",
#                 "content": """Blockchain technology has numerous applications beyond cryptocurrency:

# 1. Supply Chain Management: Track products from manufacture to delivery, ensuring authenticity and reducing fraud.

# 2. Healthcare: Securely store and share medical records while maintaining patient privacy.

# 3. Finance: Enable faster cross-border payments, reduce transaction costs, and improve transparency.

# 4. Digital Identity: Create secure, tamper-proof digital identities for individuals and organizations.

# 5. Smart Contracts: Self-executing contracts with terms directly written into code, automating agreement execution.

# 6. Voting Systems: Create transparent and tamper-proof voting systems.

# 7. Real Estate: Simplify property transactions and maintain clear ownership records.

# These applications demonstrate blockchain's potential to revolutionize various industries by providing transparency, security, and efficiency.""",
#                 "quiz_question": "Which application uses self-executing contracts with terms written into code?",
#                 "quiz_options": ["Supply Chain Management", "Digital Identity", "Smart Contracts", "Voting Systems"],
#                 "quiz_correct_answer": 2
#             }
#         ]
        
#         for chapter_data in chapters_course1:
#             chapter = Chapter(
#                 course_id=course1.id,
#                 chapter_number=chapter_data["chapter_number"],
#                 title=chapter_data["title"],
#                 content=chapter_data["content"],
#                 quiz_question=chapter_data["quiz_question"],
#                 quiz_options=json.dumps(chapter_data["quiz_options"]),
#                 quiz_correct_answer=chapter_data["quiz_correct_answer"]
#             )
#             db.add(chapter)
        
#         # Course 2: Smart Contracts Development
#         course2 = Course(
#             title="Smart Contracts with Solidity",
#             description="Master the art of creating smart contracts using Solidity programming language on the Ethereum blockchain."
#         )
#         db.add(course2)
#         db.flush()
        
#         # Course 2 Chapters
#         chapters_course2 = [
#             {
#                 "chapter_number": 1,
#                 "title": "Introduction to Smart Contracts",
#                 "content": """Smart contracts are self-executing programs stored on a blockchain that automatically execute when predetermined conditions are met. They were first proposed by Nick Szabo in 1994.

# Key features of smart contracts:
# - Autonomous: Execute automatically without intermediaries
# - Deterministic: Same input always produces same output
# - Immutable: Cannot be changed once deployed
# - Transparent: Code is visible to all network participants

# Smart contracts eliminate the need for intermediaries, reduce costs, and increase transaction speed. They are particularly useful for:
# - Financial agreements
# - Supply chain automation
# - Token creation and management
# - Decentralized applications (dApps)

# Ethereum is the most popular platform for smart contracts, using Solidity as its programming language.""",
#                 "quiz_question": "What is a key feature of smart contracts?",
#                 "quiz_options": ["They require intermediaries", "They are mutable after deployment", "They execute automatically without intermediaries", "They are invisible to network participants"],
#                 "quiz_correct_answer": 2
#             },
#             {
#                 "chapter_number": 2,
#                 "title": "Solidity Basics",
#                 "content": """Solidity is a high-level, object-oriented programming language designed for implementing smart contracts on Ethereum and other blockchain platforms.

# Basic Solidity concepts:

# 1. Contract Structure: Contracts are similar to classes in object-oriented programming
# 2. State Variables: Data stored permanently in contract storage
# 3. Functions: Define contract behavior and can modify state
# 4. Modifiers: Add conditions to functions
# 5. Events: Log information on the blockchain
# 6. Data Types: uint, int, bool, address, string, bytes, arrays, and mappings

# Example contract structure:
# ```
# pragma solidity ^0.8.0;

# contract MyContract {
#     uint public myNumber;
    
#     function setNumber(uint _num) public {
#         myNumber = _num;
#     }
# }
# ```

# Solidity is statically typed and supports inheritance, libraries, and complex user-defined types.""",
#                 "quiz_question": "What programming language is primarily used for Ethereum smart contracts?",
#                 "quiz_options": ["JavaScript", "Python", "Solidity", "Java"],
#                 "quiz_correct_answer": 2
#             },
#             {
#                 "chapter_number": 3,
#                 "title": "Functions and Visibility",
#                 "content": """Functions in Solidity define the behavior of smart contracts. Understanding function visibility is crucial for security.

# Function Visibility Modifiers:
# 1. public: Accessible from anywhere (internally and externally)
# 2. private: Only accessible within the contract
# 3. internal: Accessible within the contract and derived contracts
# 4. external: Only accessible from outside the contract

# Function State Modifiers:
# 1. view: Reads state but doesn't modify it
# 2. pure: Doesn't read or modify state
# 3. payable: Can receive Ether

# Example:
# ```
# function getValue() public view returns (uint) {
#     return myValue;
# }

# function updateValue(uint _newValue) external {
#     myValue = _newValue;
# }
# ```

# Proper use of visibility modifiers is essential for contract security and preventing unauthorized access.""",
#                 "quiz_question": "Which visibility modifier makes a function accessible only from outside the contract?",
#                 "quiz_options": ["public", "private", "internal", "external"],
#                 "quiz_correct_answer": 3
#             },
#             {
#                 "chapter_number": 4,
#                 "title": "Contract Deployment and Gas",
#                 "content": """Deploying a smart contract and executing its functions requires gas - the computational fee for operations on the Ethereum network.

# Key concepts:

# 1. Gas: Unit of computational effort required to execute operations
# 2. Gas Price: Amount of Ether you're willing to pay per unit of gas
# 3. Gas Limit: Maximum amount of gas you're willing to spend

# Deployment Process:
# 1. Compile the Solidity code to bytecode
# 2. Create a deployment transaction with the bytecode
# 3. Sign the transaction with your private key
# 4. Broadcast the transaction to the network
# 5. Miners include the transaction in a block
# 6. Contract is assigned a permanent address

# Gas Optimization Tips:
# - Use appropriate data types
# - Avoid unnecessary storage operations
# - Use events instead of storing data when possible
# - Optimize loops and conditionals

# Understanding gas mechanics is crucial for developing cost-effective smart contracts.""",
#                 "quiz_question": "What is gas in the context of Ethereum?",
#                 "quiz_options": ["A type of cryptocurrency", "A unit of computational effort required to execute operations", "A smart contract programming language", "A blockchain consensus mechanism"],
#                 "quiz_correct_answer": 1
#             }
#         ]
        
#         for chapter_data in chapters_course2:
#             chapter = Chapter(
#                 course_id=course2.id,
#                 chapter_number=chapter_data["chapter_number"],
#                 title=chapter_data["title"],
#                 content=chapter_data["content"],
#                 quiz_question=chapter_data["quiz_question"],
#                 quiz_options=json.dumps(chapter_data["quiz_options"]),
#                 quiz_correct_answer=chapter_data["quiz_correct_answer"]
#             )
#             db.add(chapter)
        
#         db.commit()
#         print("✅ Successfully seeded 2 courses with 4 chapters each!")
#         print(f"   - {course1.title}")
#         print(f"   - {course2.title}")
        
#     except Exception as e:
#         db.rollback()
#         print(f"❌ Error seeding courses: {e}")
#     finally:
#         db.close()

# if __name__ == "__main__":
#     print("🌱 Seeding courses and chapters...")
#     seed_courses()