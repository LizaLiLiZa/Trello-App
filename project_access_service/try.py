from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Генерация приватного ключа
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Сериализация приватного ключа в PEM-формат
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open("private_key.pem", "wb") as private_file:
    private_file.write(private_pem)

# Генерация публичного ключа из приватного
public_key = private_key.public_key()

# Сериализация публичного ключа в PEM-формат
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("public_key.pem", "wb") as public_file:
    public_file.write(public_pem)
