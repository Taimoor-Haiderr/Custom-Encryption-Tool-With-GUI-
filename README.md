Overview..........

This project is a Custom Encryption & Decryption Tool built using Python and Tkinter GUI. It allows users to securely encrypt and decrypt text and files (images, documents, etc.) using a custom multi-layer encryption algorithm.
The application provides a modern dark-themed interface and supports safe file handling using Base64 encoding, ensuring that encrypted files can be restored without corruption.

Features........
-- Core Functionality
--Encrypt & decrypt text
--Encrypt & decrypt files (JPG, PNG, PDF, TXT, etc.)
--Secret key-based encryption system
 Encryption Algorithm........
--Shift cipher (dynamic key-based)
--XOR encryption
--String reversal
--Multi-layer encryption logic
......File Handling..........
--Supports all file types
--Uses Base64 encoding for safe storage
--Preserves original file extension
--Restores original file after decryption
--Prevents data corruption (fixed encoding issue)
GUI Features........
--Modern dark professional UI
--Clean layout (card-style design)
--User-friendly interface
--Input & output panels
--Styled buttons and spacing
.......Extra Utilities.......
--Save output to file
--Clear all fields
--Error handling (invalid key, wrong file, etc.)
How It Works........
Encryption Process.......
User selects file or enters text
Inputs a secret key
Tool applies:
Shift cipher
Reverse string
XOR encryption
Encrypted data is converted into Base64 safe format
File saved as .enc
Decryption Process...........
Load .enc file
Enter correct key
Reverse encryption steps
Decode Base64 data
Original file restored with correct extension
Technologies Used.....
--Python
--Tkinter (GUI)
--Base64 Encoding
--File Handling (Binary & Text)
--Custom Cryptography Logic
