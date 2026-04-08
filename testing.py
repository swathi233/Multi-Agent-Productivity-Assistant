import gkeepapi
keep = gkeepapi.Keep()

success = keep.authenticate("codetesting020@gmail.com", "yzjbzkroevwyblxq")

print("Login success:", success)