# Bagger rule-based system
class Bagger:

	def __init__(self):
		self.objects = {
			0: ["Pan","Bolsa de plástico", "Mediano", "No"],
			1: ["Mermelada","Frasco", "Pequeño", "No"],
			2: ["Granola","Caja", "Grande", "No"],
			3: ["Helado","Carton", "Mediano", "Si"],
			4: ["Pepsi","Botella", "Grande", "No"],
			5: ["Chips","Bolsa de plástico", "Mediano", "No"]
		}
		self.step = ""
		self.large_bag = []
		self.large_bag_bag = []
		self.med_bag = []
		self.med_bag_bag = []
		self.small_bag = []
		self.small_bag_bag = []
		self.frozen_bag = []

		print("Bienvenido. A continuación mostramos los productos disponibles en la tienda:\n")
		print("ID\tProducto")
		for key,values in self.objects.items():
			print(key,"\t",values[0])
		print("\n")
		print("Ingrese en una línea el ID de los productos que desea")
		self.pedido_id = input().split()
		self.pedido_id = [int(item) for item in self.pedido_id ]
		
		print("Verificando su pedido:")
		pedido_letra = self.id_to_product(self.pedido_id)

		print("Pedido al momento:")
		if len(self.pedido_id) > 0:
			print("\t",pedido_letra)
			self.step = "check-order"
		else:
			print("\tLa lista está vacía. Que tenga un buen día")

		# Rules checker
		while(self.step!="final"):
			self.rule_checker()

		print("Operaciones terminadas. Bolsas generadas\n")
		
		print("Bolsas grandes:")
		if len(self.large_bag) > 0:
			self.large_bag_bag.append(self.large_bag)
		for items in self.large_bag_bag:
			print("\tBolsa:",items)
		
		print("\nBolsas medianas:")
		if len(self.med_bag) > 0:
			self.med_bag_bag.append(self.med_bag)
		for items in self.med_bag_bag:
			print("\tBolsa:",items)

		print("\nBolsas pequeñas:")
		if len(self.small_bag) > 0:
			self.small_bag_bag.append(self.small_bag)
		for items in self.small_bag_bag:
			print("\tBolsa:",items)


	def rule_checker(self):
		lista_grande = []
		lista_med = []
		lista_peq = []
		for item in self.pedido_id:
			if self.objects[item][2] == "Grande":
				lista_grande.append(item)
			elif self.objects[item][2] == "Mediano":
				lista_med.append(item)
			else:
				lista_peq.append(item)

		while(True):
			# B1
			if self.step == "check-order" and (5 in self.pedido_id) and (4 not in self.pedido_id):
				print("¿Desea agregar una Pepsi a su orden? S/N")
				ans = input()
				if ans == "S":
					self.pedido_id.append(4)	
				print("Pedido final:")
				pedido_letra = self.id_to_product(self.pedido_id)
				print("\t",pedido_letra)
				break

			#B2
			if self.step == "check-order":
				self.step = "pack-large-items"
				print("Empacando objetos grandes...")
				break

			#B3
			if self.step == "pack-large-items" and len(lista_grande) > 0 and (4 in lista_grande) and len(self.large_bag) < 6:
				self.large_bag.append(self.objects[4][0])
				self.pedido_id.remove(4)
				break

			#B4
			if self.step == "pack-large-items" and len(lista_grande) > 0 and len(self.large_bag) < 6:
				item = lista_grande.pop()
				self.large_bag.append(self.objects[item][0])
				self.pedido_id.remove(item)
				break

			#B5
			if self.step == "pack-large-items" and len(lista_grande) > 0:
				self.get_new_bag()
				break

			#B6
			if self.step == "pack-large-items":
				self.step = "pack-medium-items"
				print("Empacando objetos medianos...")
				break

			#B7
			if self.step == "pack-medium-items" and len(lista_med) > 0 and len(self.med_bag) < 6 and (3 in lista_med) and (3 not in self.frozen_bag):
				self.frozen_bag.append(self.objects[3][0])
				self.med_bag.append(self.frozen_bag)
				self.frozen_bag = []
				self.pedido_id.remove(3)
				break

			#B8
			if self.step == "pack-medium-items" and len(lista_med) > 0 and len(self.med_bag) < 6:
				item = lista_med.pop()
				self.med_bag.append(self.objects[item][0])
				self.pedido_id.remove(item)
				break

			#B9
			if self.step == "pack-medium-items" and len(lista_med) > 0 :
				self.get_new_bag()
				break

			#B10
			if self.step == "pack-medium-items" :
				self.step = "pack-small-items"
				print("Empacando objetos pequeños...")
				break

			#B11
			if self.step == "pack-small-items" and len(lista_peq) > 0 and len(self.small_bag) < 6 and (4 not in self.small_bag):
				item = lista_peq.pop()
				self.small_bag.append(self.objects[item][0])
				self.pedido_id.remove(item)
				break

			#B12
			if self.step == "pack-small-items" and len(lista_peq) > 0 and len(self.small_bag) < 6:
				item = lista_peq.pop()
				self.small_bag.append(self.objects[item][0])
				self.pedido_id.remove(item)
				break

			#B13
			if self.step == "pack-small-items" and len(lista_peq) > 0:
				self.get_new_bag()
				break

			#B14
			if self.step == "pack-small-items":
				self.step="final"
				break

	def get_new_bag(self):
		if self.step == "pack-large-items":
			self.large_bag_bag.append(self.large_bag)
			self.large_bag = []
		elif self.step == "pack-medium-items":
			self.med_bag_bag.append(self.med_bag)
			self.med_bag = []
		else:
			self.small_bag_bag.append(self.small_bag)
			self.small_bag = []


	def id_to_product(self,lista_elem):
		pedido_letra = ""
		for item in lista_elem:
			if item in self.objects.keys():
				pedido_letra += self.objects[item][0] + " "
			else:
				print("\tNo existe el producto con ID %d. Eliminado de la lista." % item)
		return pedido_letra

if __name__ == "__main__":
	Bagger()


