import hashlib

#Құжат мәтіні
document = "Mukhambetzhan Aslan"

#SHA-256 хэшін есептеу
hash_object = hashlib.sha256(document.encode())
hash_hex = hash_object.hexdigest()

print("Құжаттың SHA-256 хэші:", hash_hex)




