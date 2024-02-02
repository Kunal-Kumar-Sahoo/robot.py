class Employee:
    company = "Appl"

    def __init__(self, name, emp_id, salary):
        self.name = name
        self.emp_id = emp_id
        self.salary = salary

    def display_info(self):
        print(f"{self.name} (ID: {self.emp_id}) works for {self.company}.")
        print(f"Salary: ${self.salary} per year.")

    def apply_raise(self, percentage):
        self.salary *= (1 + percentage / 100) # salary = salary * (% calculation)
        print(f"Salary after {percentage}% raise: ${self.salary} per year.")

# Example usage:
employee1 = Employee("Alice", 1001, 50000)
employee2 = Employee("Bob", 1002, 60000)

employee1.display_info()
employee2.apply_raise(10)
