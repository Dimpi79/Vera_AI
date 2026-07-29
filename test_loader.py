from services.loader import DatasetLoader

loader = DatasetLoader()
loader.load_all()

print("\n========== DATASET SUMMARY ==========")

print(f"Categories : {len(loader.categories)}")
print(f"Merchants  : {len(loader.merchants)}")
print(f"Customers  : {len(loader.customers)}")
print(f"Triggers   : {len(loader.triggers)}")

print("\n---------- SAMPLE RECORDS ----------")

print("\nMerchant")
print(loader.merchants[0]["merchant_id"])
print(loader.merchants[0]["identity"]["name"])

print("\nCustomer")
print(loader.customers[0]["customer_id"])
print(loader.customers[0]["identity"]["name"])

print("\nTrigger")
print(loader.triggers[0]["id"])
print(loader.triggers[0]["kind"])

print("\n---------- LOOKUP TESTS ----------")

merchant = loader.get_merchant(loader.merchants[0]["merchant_id"])
customer = loader.get_customer(loader.customers[0]["customer_id"])
trigger = loader.get_trigger(loader.triggers[0]["id"])

print("Merchant Lookup :", merchant["identity"]["name"])
print("Customer Lookup :", customer["identity"]["name"])
print("Trigger Lookup  :", trigger["kind"])