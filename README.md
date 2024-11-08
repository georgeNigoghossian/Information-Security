# Information Security Project 🔒

A secure **client-server** system designed for academic environments, enabling secure interactions between students and professors. This project prioritizes **confidentiality**, **integrity**, **authentication**, and **authorization**, providing a robust framework for secure communication.

## Project Overview

This small project was developed to simulate a secure communication system within a university setting, with security mechanisms integrated to protect data and verify user identities. It follows a structured, multi-stage approach to implement various security protocols, including encryption, digital signatures, and certificate validation.

### Key Features

- **Confidentiality & Encryption**: Secure data transmission using symmetric and hybrid encryption protocols to protect sensitive information.
- **Digital Signatures (DS)**: Ensures data integrity and non-repudiation, verifying that transmitted information has not been altered.
- **Authentication & Authorization**: Verifies user identity and access permissions, using certificates and session-based verification.
- **Digital Certificates**: Signed certificates for identity verification of students and professors, managed by a trusted Certificate Authority (CA).

## Project Phases

1. **Client-Server Setup**: 
   - A server-client model, allowing students and professors to connect securely.
   - Multi-threaded server to handle multiple requests simultaneously.
   - User registration and login, with identity validation via username and password.

2. **Symmetric Encryption for Confidentiality**:
   - Secure data transmission using shared session keys for encryption.
   - Protects user information such as student ID, contact details, and address during transmission.

3. **Hybrid Encryption for Enhanced Security**:
   - Uses **PGP (Pretty Good Privacy)** encryption to safeguard data exchanges.
   - Generates unique public-private key pairs for clients and the server, performing handshakes and key exchanges at each session.

4. **Digital Signatures (DS)**:
   - Implements digital signatures to ensure message authenticity and prevent data tampering.
   - Non-repudiation support, logging and verifying data exchanges with timestamps.

5. **Digital Certificate Authentication**:
   - Uses CA-issued certificates to authenticate identities, verifying the professor’s identity using **signed certificates**.
   - Supports client certificates for students, enabling role-based permissions and access control.

## Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/georgeNigoghossian/Information-Security.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```
4. Run a client (students or professors):
   ```bash
   python client.py
   ```
