
print('-----------------------Object – Thể hiện cụ thể của Class-------------')
from DogNoConstructor import Dog

dog = Dog()

print(dog.legs)
print(dog.ears)
print(dog.breed)
print(dog.age)
print(dog.color)

print('------------Constructor – Khởi tạo object--------------')

from Dog import Dog


milo = Dog("goldendoodle", 5, "yellow")
lucky = Dog("husky", 3, "white")
# print(Dog.bark()) #lỗi vì chỉ import Object Dog

print(milo.breed, milo.age)
print(lucky.breed, lucky.age)


# Trụ cột,Ý nghĩa chính,Ví dụ thực tế trong FastAPI
# Encapsulation,"Đóng gói dữ liệu + hành vi, ẩn chi tiết bên trong",Pydantic model ẩn validation logic
# Abstraction,Chỉ lộ ra những gì cần thiết,"User chỉ thấy API endpoint, không thấy DB"
# Inheritance,Class con kế thừa từ class cha,"BaseModel → UserModel, AdminModel kế thừa"
# Polymorphism,Cùng phương thức nhưng hành vi khác nhau,Các endpoint cùng dùng .dict() nhưng khác dữ liệu