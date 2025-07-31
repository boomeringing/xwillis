# RAM-Level Encryption with 88 Key Instrument

This document outlines a conceptual technique for generating encryption keys using the full range of a piano (88 keys) as the base instrument. The approach is intended for reference implementations on both x32 and x64 architecture.

## Concept

1. Each piano key is assigned a unique byte value (0-87).
2. A song or sequence played on the piano becomes the seed for a pseudo-random key stream.
3. The sequence is recorded and hashed, then used as a key for encrypting and decrypting data in memory.
4. On an x32 system, the generated key is truncated to 32 bits; on x64, it uses the full 64 bits or more.

## Example Workflow

1. Start with an initial melody or pattern involving all 88 keys.
2. Record the timing and order of notes to generate entropy.
3. Hash the note sequence using SHA-256 to create a base key.
4. Use this key with a stream cipher (e.g., ChaCha20) to encrypt or decrypt RAM contents.

This method uses the musical performance as an unpredictable source of randomness. While primarily educational, it demonstrates how alternative input devices can inspire encryption techniques.
