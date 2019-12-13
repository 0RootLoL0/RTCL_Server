import bcrypt

pwer = "huina2pisuna"

fghj = bcrypt.hashpw(pwer.encode("utf-8"), bcrypt.gensalt(12))
vbnm = bcrypt.hashpw(b"huina2pisuna", bcrypt.gensalt(12))



print(fghj.decode("utf-8"))
print(vbnm)



print(bcrypt.checkpw(pwer.encode("utf-8"), fghj))
print(bcrypt.checkpw(pwer.encode("utf-8"), vbnm))
