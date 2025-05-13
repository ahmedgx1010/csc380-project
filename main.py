import gi
#import mysql.connector
#from mysql.connector import Error
from datetime import datetime

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ProductViewer:
    def __init__(self, glade_file):
        # Initialize configuration and attributes
        self.init_config()
        
        # Load the UI and get references to windows
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade_file)
        self.builder.connect_signals(self)
        
        # Get references to windows
        self.main_window = self.builder.get_object("main_window")
        if not self.main_window:
            print("Error: Could not find window with ID 'main_window'")
            return

        self.customer_window = self.builder.get_object("customer_window")
        if not self.customer_window:
            print("Error: Could not find window with ID 'customer_window'")
            return

        self.manager_window = self.builder.get_object("manager_window")
        if not self.manager_window:
            print("Error: Could not find window with ID 'manager_window'")
            return
            
        self.cart_window = self.builder.get_object("cart_window")
        if not self.cart_window:
            print("Error: Could not find window with ID 'cart_window'")
            
        self.browse_window = self.builder.get_object("browse_window")
        if not self.browse_window:
            print("Error: Could not find window with ID 'browse_window'")
        
        #Get customer button and manager button
        self.customer_button = self.builder.get_object("customer_button")
        if not self.customer_button:
            print("Error: Could not find Button with ID 'customer_button'")
        else:
            self.customer_button.connect("clicked", self.on_customer_button_clicked)
        
        self.manager_button = self.builder.get_object("manager_button")
        if not self.manager_button:
            print("Error: Could not find Button with ID 'manager_button'")
        else:
            self.manager_button.connect("clicked", self.on_manager_button_clicked)


        # Get customer ID entry and new order button and my orders button
        self.customerID_entry = self.builder.get_object("customerID_entry")
        if not self.customerID_entry:
            print("Error: Could not find Entry with ID 'customerID_entry'")
        
        self.newOrder_button = self.builder.get_object("newOrder_button")
        if not self.newOrder_button:
            print("Error: Could not find Button with ID 'newOrder_button'")
        else:
            self.newOrder_button.connect("clicked", self.on_newOrder_button_clicked)
        
        self.my_orders_button = self.builder.get_object("myOrders_button")
        if not self.my_orders_button:
            print("Error: Could not find Button with ID 'myOrders_button'")
        else:
            self.my_orders_button.connect("clicked", self.on_myOrders_button_clicked)

        
        # Connect window close signals
        self.main_window.connect("destroy", Gtk.main_quit)
        if self.cart_window:
            self.cart_window.connect("delete-event", self.on_cart_window_close)
        if self.browse_window:
            self.browse_window.connect("delete-event", self.on_browse_window_close)
        if self.customer_window:
            self.customer_window.connect("delete-event", self.on_customer_window_close)
        if self.manager_window:
            self.manager_window.connect("delete-event", self.on_manager_window_close)
        
        # Store customer ID
        self.customer_id = None
        
        # Initialize windows but don't show them yet
        self.initialize_windows()
        
        # Show the customer window
        self.main_window.show_all()

    def initialize_windows(self):
        """Initialize UI components but don't show windows yet"""
        # Get references to all widgets
        self.get_widget_references()
        
        # Set up the cart TreeView
        self.setup_cart_treeview()
        
        # Configure the quantity spinner
        self.configure_quantity_spinner()
        
        # Set up the browse TreeView (but don't load data yet)
        self.setup_treeview()
        
        # Initialize the grand total to zero
        self.update_grand_total()
        
        # Connect buttons
        self.connect_buttons()
    
        # Set up the my orders TreeView
        self.setup_myorders_treeview()

        # Set up the warranty TreeView
        self.setup_warranty_treeview()

        # Set up the orders TreeView
        self.setup_orders_treeview()

        # Set up the customers TreeView
        self.setup_customers_treeview()

        # Set up the stock TreeView
        self.setup_stock_treeview()

        # Set up the bundle TreeView
        self.setup_bundle_treeview()
        
        # Set up the bundle products TreeView
        self.setup_bundle_products_treeview()

    def on_customer_button_clicked(self, button):
        self.main_window.hide()
        self.customer_window.show_all()
    
    def on_customer_window_close(self, window, event):
        self.customer_window.hide()
        self.main_window.show_all()

    def on_manager_button_clicked(self, button):
        self.main_window.hide()
        self.manager_window.show_all()

    def on_manager_window_close(self, window, event):
        self.manager_window.hide()
        self.main_window.show()

    def on_warranty_button_clicked(self, button):
        """Handle click on the warranty button"""
        # Load warranty data
        self.load_warranty_data()
        
        # Hide manager window
        self.manager_window.hide()
        
        # Show warranty window
        if self.warranty_window:
            self.warranty_window.show_all()
        else:
            self.show_error_dialog("Warranty window not found.")

    def on_warranty_window_close(self, window, event):
        """Handle warranty window close event"""
        # Hide warranty window and show manager window
        self.warranty_window.hide()
        self.manager_window.show_all()
        
        # Return True to prevent the default handler from being called
        return True
    
    def on_orders_button_clicked(self, button):
        """Handle click on the orders button in manager window"""
        # Load all orders data
        self.load_all_orders()
        
        # Hide manager window
        self.manager_window.hide()
        
        # Show orders window
        if self.orders_window:
            self.orders_window.show_all()
        else:
            self.show_error_dialog("Orders window not found.")

    def on_orders_window_close(self, window, event):
        """Handle orders window close event"""
        # Hide orders window and show manager window
        self.orders_window.hide()
        self.manager_window.show_all()
        
        # Return True to prevent the default handler from being called
        return True

    def on_customerManagement_button_clicked(self, button):
        """Handle click on the customer management button"""
        # Load customer data
        self.load_customers()
        
        # Hide manager window
        self.manager_window.hide()
        
        # Show customer management window
        if self.customerManagement_window:
            self.customerManagement_window.show_all()
        else:
            self.show_error_dialog("Customer Management window not found.")

    def on_customerManagement_window_close(self, window, event):
        """Handle customer management window close event"""
        # Hide customer management window and show manager window
        self.customerManagement_window.hide()
        self.manager_window.show_all()
        
        # Return True to prevent the default handler from being called
        return True

    def on_addCustomer_button_clicked(self, button):
        """Handle click on add customer button"""
        # Clear any previous input
        if self.customerName_entry:
            self.customerName_entry.set_text("")
        if self.customerPhone_entry:
            self.customerPhone_entry.set_text("")
        if self.customerEmail_entry:
            self.customerEmail_entry.set_text("")
        if self.customerAddress_entry:
            self.customerAddress_entry.set_text("")
        
        # Hide customer management window
        self.customerManagement_window.hide()
        
        # Show add customer window
        if self.addCustomer_window:
            self.addCustomer_window.show_all()
        else:
            self.show_error_dialog("Add Customer window not found.")
            # Show customer management window again if add customer window doesn't exist
            self.customerManagement_window.show_all()

    def on_addCustomer_window_close(self, window, event):
        """Handle add customer window close event"""
        # Hide add customer window and show customer management window
        self.addCustomer_window.hide()
        self.customerManagement_window.show_all()
        
        # Return True to prevent the default handler from being called
        return True

    def on_manageBundles_button_clicked(self, button):
        """Handle click on the manage bundles button"""
        # Load bundle data
        self.load_bundles_for_management()
        
        # Hide stock window
        self.stock_window.hide()
        
        # Show bundle window
        if self.bundle_window:
            self.bundle_window.show_all()
        else:
            self.show_error_dialog("Bundle window not found.")


    def on_stock_button_clicked(self, button):
        """Handle click on the stock button"""
        # Load product data
        self.load_stock()
        
        # Hide manager window
        self.manager_window.hide()
        
        # Show stock window
        if self.stock_window:
            self.stock_window.show_all()
        else:
            self.show_error_dialog("Stock window not found.")

    def on_stock_window_close(self, window, event):
        """Handle stock window close event"""
        # Hide stock window and show manager window
        self.stock_window.hide()
        self.manager_window.show_all()
        
        # Return True to prevent the default handler from being called
        return True

    def on_addProduct_button_clicked(self, button):
        """Handle click on add product button"""
        # Clear any previous input
        if self.productName_entry:
            self.productName_entry.set_text("")
        if self.productPrice_entry:
            self.productPrice_entry.set_text("")
        if self.productStock_entry:
            self.productStock_entry.set_text("")
        
        # Hide stock window
        self.stock_window.hide()
        
        # Show add product window
        if self.addProduct_window:
            self.addProduct_window.show_all()
        else:
            self.show_error_dialog("Add Product window not found.")
            # Show stock window again if add product window doesn't exist
            self.stock_window.show_all()

    def on_addProduct_window_close(self, window, event):
        """Handle add product window close event"""
        # Hide add product window and show stock window
        self.addProduct_window.hide()
        self.stock_window.show_all()
        
        # Return True to prevent the default handler from being called
        return True

    def on_saveProduct_button_clicked(self, button):
        """Handle click on save product button"""
        # Get product information from entry fields
        name = self.productName_entry.get_text().strip() if self.productName_entry else ""
        price_text = self.productPrice_entry.get_text().strip() if self.productPrice_entry else ""
        stock_text = self.productStock_entry.get_text().strip() if self.productStock_entry else ""
        
        # Validate input
        if not name:
            self.show_error_dialog("Product name is required.")
            return
        
        # Validate price
        try:
            price = float(price_text)
            if price < 0:
                self.show_error_dialog("Price cannot be negative.")
                return
        except ValueError:
            self.show_error_dialog("Price must be a valid number.")
            return
        
        # Validate stock
        try:
            stock = int(stock_text)
            if stock < 0:
                self.show_error_dialog("Stock cannot be negative.")
                return
        except ValueError:
            self.show_error_dialog("Stock must be a whole number.")
            return
        
        # Save new product to database
        success = self.add_new_product(name, price, stock)
        
        if success:
            # Show success message
            self.show_success_dialog("Product added successfully.")
            
            # Close add product window and return to stock management
            self.addProduct_window.hide()
            
            # Refresh the product list
            self.load_stock()
            
            # Show stock window
            self.stock_window.show_all()
        else:
            # Error message is shown in add_new_product method
            pass

    def add_new_product(self, name, price, stock):
        """Add a new product to the database"""
        connection = self.connect_to_mysql()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Check if product with this name already exists
            query = "SELECT 1 FROM product WHERE Name = %s"
            cursor.execute(query, (name,))
            
            if cursor.fetchone():
                self.show_error_dialog(f"A product with the name '{name}' already exists.")
                return False
            
            # Insert the new product
            query = """
            INSERT INTO product (Name, Price, Stock)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (name, str(price), str(stock)))
            
            # Commit the transaction
            connection.commit()
            
            return True
            
        except Error as e:
            print(f"Error adding product: {e}")
            self.show_error_dialog(f"Error adding product: {e}")
            if connection:
                connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def setup_stock_treeview(self):
        """Set up the stock TreeView with columns"""
        if not self.stock_tree:
            return
        
        # Create a ListStore for products with columns:
        # [Name (str), Price (float), Stock (int)]
        self.stock_liststore = Gtk.ListStore(str, float, int)
        
        # Create a filter model for searching - correct way to create TreeModelFilter
        self.stock_filter_model = self.stock_liststore.filter_new()
        self.stock_filter_model.set_visible_func(self.stock_filter_func)
        
        # Use the filter model instead of the direct ListStore
        self.stock_tree.set_model(self.stock_filter_model)
        
        # Remove any existing columns
        for column in self.stock_tree.get_columns():
            self.stock_tree.remove_column(column)
        
        # Add columns for products
        columns = [
            ("Product Name", 250, 0, str),
            ("Price", 100, 1, float, self.price_cell_data_func),
            ("Stock", 80, 2, int)
        ]
        
        for i, (title, width, index, data_type, *args) in enumerate(columns):
            renderer = Gtk.CellRendererText()
            
            if args and args[0]:  # If a custom formatter is provided
                column = Gtk.TreeViewColumn(title, renderer)
                column.set_cell_data_func(renderer, args[0])
            else:
                column = Gtk.TreeViewColumn(title, renderer, text=index)
                
            column.set_resizable(True)
            column.set_min_width(width)
            column.set_sort_column_id(index)
            self.stock_tree.append_column(column)
        
        # Connect row-activated signal for product details (optional)
        self.stock_tree.connect("row-activated", self.on_product_row_activated)
        
        # Add selection handling to update add stock button sensitivity
        selection = self.stock_tree.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        selection.connect("changed", self.on_stock_selection_changed)


    def load_stock(self):
        """Load all products for the stock window"""
        connection = self.connect_to_mysql()
        if not connection:
            return
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query to get all products
            query = "SELECT Name, Price, Stock FROM product ORDER BY Name"
            cursor.execute(query)
            products = cursor.fetchall()
            
            # Clear existing data
            self.stock_liststore.clear()
            
            # Add each product to the list
            for product in products:
                try:
                    price = float(product['Price']) if product['Price'] is not None else 0.0
                    stock = int(product['Stock']) if product['Stock'] is not None else 0
                    
                    self.stock_liststore.append([
                        product['Name'],
                        price,
                        stock
                    ])
                except (ValueError, TypeError) as e:
                    print(f"Error processing product {product['Name']}: {e}")
                
        except Error as e:
            print(f"Error loading products: {e}")
            self.show_error_dialog(f"Error loading products: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        # After loading data, refilter the model
        if hasattr(self, 'stock_filter_model') and self.stock_filter_model:
            self.stock_filter_model.refilter()

    def configure_stock_quantity_spinner(self):
        """Configure the stock quantity spinner"""
        if not self.stock_quantity:
            return
        
        # Set the range (minimum, maximum)
        self.stock_quantity.set_range(1, 1000)  # Allow adding 1 to 1000 items
        
        # Set the default value
        self.stock_quantity.set_value(1)
        
        # Set the step increment (how much it changes when +/- is clicked)
        self.stock_quantity.set_increments(1, 10)  # Small step 1, large step 10
        
        # Make sure it's editable
        self.stock_quantity.set_editable(True)
        
        # Set numeric mode
        self.stock_quantity.set_numeric(True)
        
        # Update the policy to update the value when changed
        self.stock_quantity.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)

    def on_stock_selection_changed(self, selection):
        """Handle selection change in stock tree"""
        model, iter = selection.get_selected()
        
        # Enable or disable add stock button based on selection
        if self.addStock_button:
            self.addStock_button.set_sensitive(iter is not None)

    def on_stock_search_changed(self, entry):
        """Handle changes to the search entry"""
        # Refilter the stock list
        self.stock_filter_model.refilter()

    def stock_filter_func(self, model, iter, data):
        """Filter function for the stock list"""
        if not self.stock_search:
            return True
        
        search_text = self.stock_search.get_text().lower()
        
        # If search is empty, show all rows
        if not search_text:
            return True
        
        # Get the product name
        product_name = model.get_value(iter, 0).lower()
        
        # Show if the search text is in the product name
        return search_text in product_name

    def on_addStock_button_clicked(self, button):
        """Handle adding stock to a product"""
        # Get the selected product
        selection = self.stock_tree.get_selection()
        model, iter = selection.get_selected()
        
        if not iter:
            self.show_error_dialog("Please select a product.")
            return
        
        # If using filter model, we need to convert iter to the base model
        if isinstance(model, Gtk.TreeModelFilter):
            child_iter = model.convert_iter_to_child_iter(iter)
            product_name = model.get_model().get_value(child_iter, 0)
            current_stock = model.get_model().get_value(child_iter, 2)
        else:
            product_name = model.get_value(iter, 0)
            current_stock = model.get_value(iter, 2)
        
        # Get the quantity to add
        quantity_to_add = self.stock_quantity.get_value_as_int()
        
        if quantity_to_add <= 0:
            self.show_error_dialog("Please enter a positive quantity.")
            return
        
        # Calculate new stock
        new_stock = current_stock + quantity_to_add
        
        # Update the database
        success = self.update_product_stock(product_name, new_stock)
        
        if success:
            # Show success message
            self.show_success_dialog(f"Added {quantity_to_add} items to {product_name}. New stock: {new_stock}")
            
            # Update the stock liststore
            if isinstance(model, Gtk.TreeModelFilter):
                model.get_model().set_value(child_iter, 2, new_stock)
            else:
                model.set_value(iter, 2, new_stock)
            
            # Reset the quantity spinner to 1
            self.stock_quantity.set_value(1)
        else:
            # Error message is shown in update_product_stock method
            pass

    def update_product_stock(self, product_name, new_stock):
        """Update the stock of a product in the database"""
        connection = self.connect_to_mysql()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Update the stock
            query = "UPDATE product SET Stock = %s WHERE Name = %s"
            cursor.execute(query, (str(new_stock), product_name))
            
            # Commit the transaction
            connection.commit()
            
            # Check if the update was successful
            if cursor.rowcount > 0:
                return True
            else:
                self.show_error_dialog(f"Product '{product_name}' not found.")
                return False
            
        except Error as e:
            print(f"Error updating stock: {e}")
            self.show_error_dialog(f"Error updating stock: {e}")
            if connection:
                connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_product_row_activated(self, treeview, path, column):
        """Handle double-click on product row (optional)"""
        model = treeview.get_model()
        iter = model.get_iter(path)
        
        if iter:
            # Get the selected product details
            product_name = model.get_value(iter, 0)
            product_price = model.get_value(iter, 1)
            product_stock = model.get_value(iter, 2)
            
            # Show product details
            details = f"Product Details:\n\n"
            details += f"Name: {product_name}\n"
            details += f"Price: ${product_price:.2f}\n"
            details += f"Stock: {product_stock}\n"
            
            # Show the details
            self.show_info_dialog(details)

    def on_saveCustomer_button_clicked(self, button):
        """Handle click on save customer button"""
        # Get customer information from entry fields
        name = self.customerName_entry.get_text().strip() if self.customerName_entry else ""
        phone = self.customerPhone_entry.get_text().strip() if self.customerPhone_entry else ""
        email = self.customerEmail_entry.get_text().strip() if self.customerEmail_entry else ""
        address = self.customerAddress_entry.get_text().strip() if self.customerAddress_entry else ""
        
        # Validate input
        if not name:
            self.show_error_dialog("Customer name is required.")
            return
        
        # Save new customer to database
        success = self.add_new_customer(name, phone, email, address)
        
        if success:
            # Show success message
            self.show_success_dialog("Customer added successfully.")
            
            # Close add customer window and return to customer management
            self.addCustomer_window.hide()
            
            # Refresh the customer list
            self.load_customers()
            
            # Show customer management window
            self.customerManagement_window.show_all()
        else:
            # Error message is shown in add_new_customer method
            pass

    def load_customers(self):
        """Load all customers for the customer management window"""
        connection = self.connect_to_mysql()
        if not connection:
            return
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query to get all customers
            query = "SELECT * FROM customer ORDER BY Name"
            cursor.execute(query)
            customers = cursor.fetchall()
            
            # Clear existing data
            self.customers_liststore.clear()
            
            # Add each customer to the list
            for customer in customers:
                self.customers_liststore.append([
                    customer['CustomerID'],
                    customer['Name'],
                    customer['phone'],
                    customer['Email'],
                    customer['Address']
                ])
                
        except Error as e:
            print(f"Error loading customers: {e}")
            self.show_error_dialog(f"Error loading customers: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_customer_row_activated(self, treeview, path, column):
        """Handle double-click on customer row (optional)"""
        model = treeview.get_model()
        iter = model.get_iter(path)
        
        if iter:
            # Get the selected customer details
            customer_id = model.get_value(iter, 0)
            customer_name = model.get_value(iter, 1)
            customer_phone = model.get_value(iter, 2)
            customer_email = model.get_value(iter, 3)
            customer_address = model.get_value(iter, 4)
            
            # You could show customer details, edit customer, etc.
            details = f"Customer Details:\n\n"
            details += f"ID: {customer_id}\n"
            details += f"Name: {customer_name}\n"
            details += f"Phone: {customer_phone}\n"
            details += f"Email: {customer_email}\n"
            details += f"Address: {customer_address}\n"
            
            # Show the details
            self.show_info_dialog(details)

    def add_new_customer(self, name, phone, email, address):
        """Add a new customer to the database"""
        connection = self.connect_to_mysql()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Generate a new customer ID
            query = "SELECT MAX(CustomerID) as max_id FROM customer"
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result[0] is not None:
                new_id = result[0] + 1
            else:
                new_id = 1
            
            # Insert the new customer
            query = """
            INSERT INTO customer (CustomerID, Name, phone, Email, Address)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (new_id, name, phone, email, address))
            
            # Commit the transaction
            connection.commit()
            
            return True
            
        except Error as e:
            print(f"Error adding customer: {e}")
            self.show_error_dialog(f"Error adding customer: {e}")
            if connection:
                connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def setup_customers_treeview(self):
        """Set up the customers TreeView with columns"""
        if not self.customers_tree:
            return
        
        # Create a ListStore for customers with columns:
        # [ID (int), Name (str), Phone (str), Email (str), Address (str)]
        self.customers_liststore = Gtk.ListStore(int, str, str, str, str)
        self.customers_tree.set_model(self.customers_liststore)
        
        # Remove any existing columns
        for column in self.customers_tree.get_columns():
            self.customers_tree.remove_column(column)
        
        # Add columns for customers
        columns = [
            ("ID", 80, 0, int),
            ("Name", 200, 1, str),
            ("Phone", 120, 2, str),
            ("Email", 200, 3, str),
            ("Address", 250, 4, str)
        ]
        
        for i, (title, width, index, data_type) in enumerate(columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=index)
            column.set_resizable(True)
            column.set_min_width(width)
            column.set_sort_column_id(index)
            self.customers_tree.append_column(column)
        
        # Connect row-activated signal for customer details (optional)
        self.customers_tree.connect("row-activated", self.on_customer_row_activated)



    def setup_orders_treeview(self):
        """Set up the orders TreeView with columns"""
        if not self.orders_tree:
            return
        
        # Create a ListStore for orders with columns:
        # [OrderID (int), Date (str), Customer ID (int), Customer Name (str), Total (float), Items Count (int)]
        self.orders_liststore = Gtk.ListStore(int, str, int, str, float, int)
        self.orders_tree.set_model(self.orders_liststore)
        
        # Remove any existing columns
        for column in self.orders_tree.get_columns():
            self.orders_tree.remove_column(column)
        
        # Add columns for the orders
        columns = [
            ("Order ID", 80, 0, int),
            ("Date", 150, 1, str),
            ("Customer ID", 100, 2, int),
            ("Customer Name", 200, 3, str),
            ("Total", 100, 4, float, self.price_cell_data_func),
            ("Items", 80, 5, int)
        ]
        
        for i, (title, width, index, data_type, *args) in enumerate(columns):
            renderer = Gtk.CellRendererText()
            
            if args and args[0]:  # If a custom formatter is provided
                column = Gtk.TreeViewColumn(title, renderer)
                column.set_cell_data_func(renderer, args[0])
            else:
                column = Gtk.TreeViewColumn(title, renderer, text=index)
                    
            column.set_resizable(True)
            column.set_min_width(width)
            column.set_sort_column_id(index)
            self.orders_tree.append_column(column)
        
        # Connect row-activated signal for order details
        self.orders_tree.connect("row-activated", self.on_order_row_activated_manager)

    def load_all_orders(self):
        """Load all orders data for manager view"""
        connection = self.connect_to_mysql()
        if not connection:
            return
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query to get all orders with customer information
            query = """
            SELECT 
                o.OrderID, 
                o.OrderDate, 
                o.Cost,
                o.Customer_CustomerID,
                c.Name AS CustomerName
            FROM `order` o
            LEFT JOIN customer c ON o.Customer_CustomerID = c.CustomerID
            ORDER BY o.OrderDate DESC
            """
            cursor.execute(query)
            orders = cursor.fetchall()
            
            # Clear existing data
            self.orders_liststore.clear()
            
            # Add each order to the list
            for order in orders:
                order_id = order['OrderID']
                order_date = order['OrderDate']
                customer_id = order['Customer_CustomerID']
                customer_name = order['CustomerName'] or "Unknown"
                order_cost = float(order['Cost']) if order['Cost'] is not None else 0.0
                
                # Count the number of items in this order
                items_count = self.count_order_items(cursor, order_id, customer_id)
                
                # Add to ListStore
                self.orders_liststore.append([
                    order_id,
                    order_date,
                    customer_id,
                    customer_name,
                    order_cost,
                    items_count
                ])
                
        except Error as e:
            print(f"Error loading orders: {e}")
            self.show_error_dialog(f"Error loading orders: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_order_row_activated_manager(self, treeview, path, column):
        """Handle double-click on order row in manager view"""
        model = treeview.get_model()
        iter = model.get_iter(path)
        
        if iter:
            # Get the selected order details
            order_id = model.get_value(iter, 0)
            customer_id = model.get_value(iter, 2)
            
            # Load and show order details
            self.show_order_details(order_id, customer_id)

    def show_order_details(self, order_id, customer_id):
        """Show detailed information about an order"""
        connection = self.connect_to_mysql()
        if not connection:
            return
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get order information
            order_query = """
            SELECT o.OrderID, o.OrderDate, o.Cost, c.Name AS CustomerName, 
                c.phone AS CustomerPhone, c.Email AS CustomerEmail, c.Address AS CustomerAddress
            FROM `order` o
            LEFT JOIN customer c ON o.Customer_CustomerID = c.CustomerID
            WHERE o.OrderID = %s AND o.Customer_CustomerID = %s
            """
            cursor.execute(order_query, (order_id, customer_id))
            order_info = cursor.fetchone()
            
            if not order_info:
                self.show_error_dialog(f"Order #{order_id} not found.")
                return
            
            # Get products in the order
            products_query = """
            SELECT p.Name, p.Price
            FROM product p
            JOIN order_has_product ohp ON p.Name = ohp.Product_Name
            WHERE ohp.Order_OrderID = %s AND ohp.Order_Customer_CustomerID = %s
            """
            cursor.execute(products_query, (order_id, customer_id))
            products = cursor.fetchall()
            
            # Get bundles in the order
            bundles_query = """
            SELECT b.Name, b.Discount
            FROM bundle b
            JOIN order_has_bundle ohb ON b.BundleID = ohb.Bundle_BundleID
            WHERE ohb.Order_OrderID = %s AND ohb.Order_Customer_CustomerID = %s
            """
            cursor.execute(bundles_query, (order_id, customer_id))
            bundles = cursor.fetchall()
            
            # Format order details for display
            details = f"Order #{order_id} Details\n\n"
            details += f"Date: {order_info['OrderDate']}\n"
            details += f"Total Cost: ${float(order_info['Cost']):.2f}\n\n"
            
            details += f"Customer Information:\n"
            details += f"ID: {customer_id}\n"
            details += f"Name: {order_info['CustomerName']}\n"
            details += f"Phone: {order_info['CustomerPhone']}\n"
            details += f"Email: {order_info['CustomerEmail']}\n"
            details += f"Address: {order_info['CustomerAddress']}\n\n"
            
            if products:
                details += f"Products:\n"
                for product in products:
                    details += f"- {product['Name']}: ${float(product['Price']):.2f}\n"
            
            if bundles:
                details += f"\nBundles:\n"
                for bundle in bundles:
                    discount = bundle['Discount'] or "0"
                    details += f"- {bundle['Name']} (Discount: {discount}%)\n"
                    
                    # Get products in this bundle
                    bundle_products_query = f"""
                    SELECT p.Name, p.Price
                    FROM product p
                    JOIN bundle_has_product bhp ON p.Name = bhp.Product_Name
                    JOIN bundle b ON bhp.Bundle_BundleID = b.BundleID
                    WHERE b.Name = '{bundle['Name']}'
                    """
                    cursor.execute(bundle_products_query)
                    bundle_products = cursor.fetchall()
                    
                    for bp in bundle_products:
                        details += f"  • {bp['Name']}: ${float(bp['Price']):.2f}\n"
            
            # Show the details
            self.show_info_dialog(details)
            
        except Error as e:
            print(f"Error fetching order details: {e}")
            self.show_error_dialog(f"Error loading order details: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def setup_warranty_treeview(self):
        """Set up the warranty TreeView with columns"""
        if not self.warranty_tree:
            return
        
        # Create a ListStore for warranty with columns:
        # [Bundle Name (str), Customer ID (int), Purchase Date (str), Duration (str), Status (str)]
        self.warranty_liststore = Gtk.ListStore(str, int, str, str, str)
        self.warranty_tree.set_model(self.warranty_liststore)
        
        # Remove any existing columns
        for column in self.warranty_tree.get_columns():
            self.warranty_tree.remove_column(column)
        
        # Add columns for the warranty
        columns = [
            ("Bundle", 200, 0, str),
            ("Customer ID", 100, 1, int),
            ("Purchase Date", 150, 2, str),
            ("Duration", 150, 3, str),
            ("Status", 100, 4, str)
        ]
        
        for i, (title, width, index, data_type) in enumerate(columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=index)
            column.set_resizable(True)
            column.set_min_width(width)
            column.set_sort_column_id(index)
            self.warranty_tree.append_column(column)
        
        # Connect row-activated signal for details
        self.warranty_tree.connect("row-activated", self.on_warranty_row_activated)

    def load_warranty_data(self):
        """Load warranty data from the warranty table"""
        connection = self.connect_to_mysql()
        if not connection:
            return
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query to get warranty information joined with bundle data
            query = """
            SELECT 
                w.WarrantyID,
                w.Duration,
                w.Coverage,
                b.Name AS bundle_name,
                b.BundleID
            FROM warranty w
            JOIN bundle b ON w.Bundle_BundleID = b.BundleID
            """
            cursor.execute(query)
            warranty_items = cursor.fetchall()
            
            # Clear existing data in the warranty tree
            self.warranty_liststore.clear()
            
            # For each warranty, find orders that include this bundle
            for item in warranty_items:
                bundle_id = item['BundleID']
                bundle_name = item['bundle_name']
                duration = item['Duration']
                coverage = item['Coverage']
                
                # Find orders for this bundle - using format string with explicit value instead of parameter
                # since some MariaDB configurations may have issues with %s placeholders
                order_query = f"""
                SELECT 
                    o.OrderID,
                    o.Customer_CustomerID,
                    o.OrderDate
                FROM `order` o
                JOIN order_has_bundle ohb ON o.OrderID = ohb.Order_OrderID 
                    AND o.Customer_CustomerID = ohb.Order_Customer_CustomerID
                WHERE ohb.Bundle_BundleID = {bundle_id}
                """
                cursor.execute(order_query)  # No parameters needed now
                orders = cursor.fetchall()
                
                # Add a row for each order of this bundle with warranty
                for order in orders:
                    customer_id = order['Customer_CustomerID']
                    purchase_date = order['OrderDate']
                    
                    # Calculate warranty status based on purchase date and duration
                    # This assumes Duration is stored as "X Years" or "X Months"
                    status = "Unknown"
                    try:
                        if "year" in duration.lower():
                            years = int(duration.split()[0])
                            expiry_date_query = f"SELECT DATE_ADD('{purchase_date}', INTERVAL {years} YEAR) as expiry"
                        elif "month" in duration.lower():
                            months = int(duration.split()[0])
                            expiry_date_query = f"SELECT DATE_ADD('{purchase_date}', INTERVAL {months} MONTH) as expiry"
                        else:
                            # Default to 1 year if format is unknown
                            expiry_date_query = f"SELECT DATE_ADD('{purchase_date}', INTERVAL 1 YEAR) as expiry"
                        
                        cursor.execute(expiry_date_query)
                        expiry_date_result = cursor.fetchone()
                        expiry_date = expiry_date_result['expiry']
                        
                        # Check if warranty is still active
                        current_date_query = "SELECT NOW() as `current_date`"
                        cursor.execute(current_date_query)
                        current_date_result = cursor.fetchone()
                        current_date = current_date_result['current_date']
                        
                        if current_date <= expiry_date:
                            status = "Active"
                        else:
                            status = "Expired"
                    except (ValueError, TypeError) as e:
                        print(f"Error calculating warranty status: {e}")
                        status = "Unknown"
                    
                    # Add to ListStore - we'll use a modified structure to match the schema
                    self.warranty_liststore.append([
                        bundle_name,
                        customer_id,
                        purchase_date,
                        duration,
                        status
                    ])
            
        except Error as e:
            print(f"Error loading warranty data: {e}")
            self.show_error_dialog(f"Error loading warranty data: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_warranty_row_activated(self, treeview, path, column):
        """Handle double-click on warranty row"""
        model = treeview.get_model()
        iter = model.get_iter(path)
        
        if iter:
            # Get the selected warranty details
            bundle_name = model.get_value(iter, 0)
            customer_id = model.get_value(iter, 1)
            purchase_date = model.get_value(iter, 2)
            duration = model.get_value(iter, 3)
            status = model.get_value(iter, 4)
            
            # Load additional details about the bundle and customer
            connection = self.connect_to_mysql()
            if not connection:
                return
            
            try:
                cursor = connection.cursor(dictionary=True)
                
                # Get bundle details including coverage
                query = """
                SELECT w.Coverage, b.Discount
                FROM warranty w
                JOIN bundle b ON w.Bundle_BundleID = b.BundleID
                WHERE b.Name = %s
                """
                cursor.execute(query, (bundle_name,))
                bundle_info = cursor.fetchone()
                
                # Get customer details
                customer_info = self.get_customer_info(customer_id)
                
                # Get products in the bundle
                products_query = """
                SELECT p.Name, p.Price
                FROM product p
                JOIN bundle_has_product bhp ON p.Name = bhp.Product_Name
                JOIN bundle b ON bhp.Bundle_BundleID = b.BundleID
                WHERE b.Name = %s
                """
                cursor.execute(products_query, (bundle_name,))
                products = cursor.fetchall()
                
                # Format details for display
                details = f"Warranty Details:\n\n"
                details += f"Bundle: {bundle_name}\n"
                if bundle_info:
                    details += f"Coverage: {bundle_info.get('Coverage', 'N/A')}\n"
                    details += f"Discount: {bundle_info.get('Discount', '0')}%\n"
                details += f"Purchase Date: {purchase_date}\n"
                details += f"Warranty Duration: {duration}\n"
                details += f"Status: {status}\n\n"
                
                if customer_info:
                    details += f"Customer Information:\n"
                    details += f"ID: {customer_id}\n"
                    details += f"Name: {customer_info.get('Name', 'N/A')}\n"
                    details += f"Phone: {customer_info.get('phone', 'N/A')}\n"
                    details += f"Email: {customer_info.get('Email', 'N/A')}\n"
                    details += f"Address: {customer_info.get('Address', 'N/A')}\n\n"
                
                if products:
                    details += f"Products in Bundle:\n"
                    for product in products:
                        details += f"- {product['Name']}: ${float(product['Price']):.2f}\n"
                
                # Show the details
                self.show_info_dialog(details)
                
            except Error as e:
                print(f"Error fetching warranty details: {e}")
                
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def get_customer_info(self, customer_id):
        """Get customer information by ID"""
        connection = self.connect_to_mysql()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM customer WHERE CustomerID = %s"
            cursor.execute(query, (customer_id,))
            customer = cursor.fetchone()
            
            return customer
            
        except Error as e:
            print(f"Error fetching customer info: {e}")
            return None
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_myOrders_button_clicked(self, button):
        """Handle click on the My Orders button"""
        if not self.customerID_entry:
            self.show_error_dialog("Customer ID entry not found.")
            return
        
        # Get the customer ID from the entry
        customer_id_text = self.customerID_entry.get_text().strip()
        
        if not customer_id_text:
            self.show_error_dialog("Please enter a Customer ID.")
            return
        
        try:
            # Convert to integer
            customer_id = int(customer_id_text)
            
            # Validate if customer exists
            if self.validate_customer(customer_id):
                # Store the customer ID
                self.customer_id = customer_id
                
                # Load the customer's orders
                self.load_customer_orders(customer_id)
                
                # Hide customer window
                self.customer_window.hide()
                
                # Show my orders window
                self.my_orders_window = self.builder.get_object("myOrders_window")
                if self.my_orders_window:
                    self.my_orders_window.show_all()
                else:
                    self.show_error_dialog("My Orders window not found.")
            else:
                self.show_error_dialog(f"Customer with ID {customer_id} not found.")
        except ValueError:
            self.show_error_dialog("Please enter a valid numeric Customer ID.")

    def connect_buttons(self):
        """Connect all buttons to their handlers"""
        # Connect browse button
        self.browse_button = self.builder.get_object("browse_button")
        if not self.browse_button:
            print("Error: Could not find Button with ID 'browse_button'")
        else:
            self.browse_button.connect("clicked", self.on_browse_button_clicked)
        
        # Connect remove button
        self.remove_button = self.builder.get_object("remove_button")
        if not self.remove_button:
            print("Error: Could not find Button with ID 'remove_button'")
        else:
            self.remove_button.connect("clicked", self.on_remove_button_clicked)
        
        # Connect checkout button
        self.checkout_button = self.builder.get_object("checkout_button")
        if not self.checkout_button:
            print("Error: Could not find Button with ID 'checkout_button'")
        else:
            self.checkout_button.connect("clicked", self.on_checkout_button_clicked)

    def on_newOrder_button_clicked(self, button):
        """Handle click on the new order button"""
        if not self.customerID_entry:
            self.show_error_dialog("Customer ID entry not found.")
            return
        
        # Get the customer ID from the entry
        customer_id_text = self.customerID_entry.get_text().strip()
        
        if not customer_id_text:
            self.show_error_dialog("Please enter a Customer ID.")
            return
        
        try:
            # Convert to integer
            customer_id = int(customer_id_text)
            
            # Validate if customer exists
            if self.validate_customer(customer_id):
                # Store the customer ID
                self.customer_id = customer_id
                
                # Hide customer window
                self.customer_window.hide()
                
                # Show cart window
                self.cart_window.show_all()
            else:
                self.show_error_dialog(f"Customer with ID {customer_id} not found.")
        except ValueError:
            self.show_error_dialog("Please enter a valid numeric Customer ID.")

    def validate_customer(self, customer_id):
        """Validate if a customer exists in the database"""
        connection = self.connect_to_mysql()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Query to check if customer exists
            query = "SELECT 1 FROM customer WHERE CustomerID = %s"
            cursor.execute(query, (customer_id,))
            
            result = cursor.fetchone()
            
            # Return True if customer exists, False otherwise
            return result is not None
            
        except Error as e:
            print(f"Error validating customer: {e}")
            self.show_error_dialog(f"Error validating customer: {e}")
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def on_cart_window_close(self, window, event):
        """Handle cart window close event"""
        # Show the customer window again and hide the cart window
        self.cart_window.hide()
        self.customer_window.show_all()
        
        # Clear the cart when returning to customer window
        if hasattr(self, 'cart_treestore'):
            self.cart_treestore.clear()
        
        # Reset customer ID
        self.customer_id = None
        
        # Return True to prevent the default handler from being called
        return True

    def init_config(self):
        """Initialize database configuration and display attributes"""
        # Database configuration
        self.db_config = {
            "host": "192.168.35.222",
            "database": "mydb",
            "user": "root",
            "password": ""
        }
        
        # Now we need three columns: Name, Discount, Price
        # For the TreeView, we'll use a TreeStore instead of a ListStore
        # Format: [(column_name, column_title, column_width, data_type), ...]
        self.attributes_to_display = [
            ("Name", "Product/Bundle Name", 200, str),
            ("Discount", "Discount (%)", 100, str),  # Discount will be a string (empty for products)
            ("Price", "Price ($)", 100, float)
        ]

        
        # Attribute to search on (change this to search different columns)
        self.search_attribute_index = 0  # Default to first column (Name)
    
    def init_ui_components(self):
        """Initialize all UI components after windows are loaded"""
        # Get references to all widgets
        self.get_widget_references()
        
        # Set up the cart TreeView
        self.setup_cart_treeview()
        
        # Configure the quantity spinner
        self.configure_quantity_spinner()
        
        # Set up the browse TreeView (but don't load data yet)
        self.setup_treeview()
        
        # Initialize the grand total to zero
        self.update_grand_total()
        
        # Connect the remove button
        self.remove_button = self.builder.get_object("remove_button")
        if not self.remove_button:
            print("Error: Could not find Button with ID 'remove_button'")
        else:
            self.remove_button.connect("clicked", self.on_remove_button_clicked)
        
        # Connect checkout button
        self.checkout_button = self.builder.get_object("checkout_button")
        if not self.checkout_button:
            print("Error: Could not find Button with ID 'checkout_button'")
        else:
            self.checkout_button.connect("clicked", self.on_checkout_button_clicked)
    
    def on_checkout_button_clicked(self, button):
        """Handle checkout button click - create an order"""
        # Check if cart is empty
        if len(self.cart_treestore) == 0:
            self.show_error_dialog("Your cart is empty. Please add items before checkout.")
            return
        
        # Use the stored customer ID
        if not self.customer_id:
            self.show_error_dialog("Customer ID not set. Please start a new order.")
            return
        
        # Verify product availability
        unavailable_items = self.check_stock_availability()
        
        if unavailable_items:
            # Show error with unavailable items
            error_message = "The following items don't have enough stock:\n\n"
            for item, available, required in unavailable_items:
                error_message += f"• {item}: {available} in stock, {required} requested\n"
            self.show_error_dialog(error_message)
            return
        
        # Get order total
        order_total = self.calculate_cart_total()
        
        # Create the order
        order_id = self.create_order(self.customer_id, order_total)
        
        if order_id:
            # Process the order items
            success = self.process_order_items(order_id, self.customer_id)
            
            if success:
                # Show success message
                self.show_success_dialog(f"Order #{order_id} has been placed successfully!")
                
                # Clear the cart
                self.cart_treestore.clear()
                self.update_grand_total()
                
                # Refresh product list to show updated stock
                self.load_data_from_mysql()
                
                # Go back to the customer window for a new order
                self.cart_window.hide()
                self.customer_window.show_all()
                
                # Reset customer ID
                self.customer_id = None
            else:
                # If processing failed, show error and delete the order
                self.show_error_dialog("Error processing your order. Please try again.")
                self.delete_order(order_id, self.customer_id)
        else:
            self.show_error_dialog("Error creating your order. Please try again.")

    def check_stock_availability(self):
        """Check if all products in the cart are available in sufficient quantity"""
        connection = self.connect_to_mysql()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # First, collect all products and their quantities from the cart
            # We need to count products both as standalone items and within bundles
            product_quantities = {}
            
            # Iterate through the entire cart treestore
            self.collect_product_quantities(self.cart_treestore, None, product_quantities)
            
            # Now check each product's stock
            unavailable_items = []
            
            for product_name, quantity in product_quantities.items():
                # Query product stock
                query = "SELECT Stock FROM product WHERE Name = %s"
                cursor.execute(query, (product_name,))
                result = cursor.fetchone()
                
                if result:
                    try:
                        available_stock = int(result['Stock'])
                        if available_stock < quantity:
                            unavailable_items.append((product_name, available_stock, quantity))
                    except (ValueError, TypeError):
                        # If stock is not a valid number, consider it unavailable
                        unavailable_items.append((product_name, 0, quantity))
                else:
                    # Product not found
                    unavailable_items.append((product_name, 0, quantity))
            
            return unavailable_items
            
        except Error as e:
            print(f"Error checking stock: {e}")
            self.show_error_dialog(f"Error checking product availability: {e}")
            return [("Database error", 0, 0)]
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def collect_product_quantities(self, model, parent_iter, product_quantities):
        """Recursively collect products and their quantities from the cart"""
        # If parent_iter is None, start at the top level
        if parent_iter is None:
            # Process all top-level items
            for i in range(model.iter_n_children(None)):
                child_iter = model.iter_nth_child(None, i)
                self.collect_product_quantities(model, child_iter, product_quantities)
            return
        
        # Get data for the current item
        item_name = model.get_value(parent_iter, 0)
        item_quantity = model.get_value(parent_iter, 2)
        item_type = model.get_value(parent_iter, 4)
        
        if item_type == "product":
            # This is a standalone product
            if item_name in product_quantities:
                product_quantities[item_name] += item_quantity
            else:
                product_quantities[item_name] = item_quantity
        elif item_type == "bundle":
            # For bundles, process all products within the bundle
            for i in range(model.iter_n_children(parent_iter)):
                child_iter = model.iter_nth_child(parent_iter, i)
                child_name = model.get_value(child_iter, 0)
                child_quantity = model.get_value(child_iter, 2)
                
                if child_name in product_quantities:
                    product_quantities[child_name] += child_quantity
                else:
                    product_quantities[child_name] = child_quantity
        elif item_type == "bundle-product":
            # Skip bundle products as they're handled by their parent bundle
            pass
        
        # Process any children
        for i in range(model.iter_n_children(parent_iter)):
            child_iter = model.iter_nth_child(parent_iter, i)
            self.collect_product_quantities(model, child_iter, product_quantities)

    def calculate_cart_total(self):
        """Calculate the total cost of the cart"""
        grand_total = 0.0
        
        # Only count top-level items (not bundle products) to avoid double counting
        for row in self.cart_treestore:
            # Get the total for this row
            total = row[3]
            grand_total += total
        
        return grand_total

    def create_order(self, customer_id, order_total):
        """Create a new order in the database"""
        connection = self.connect_to_mysql()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            
            # Get the current date
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Generate a new order ID
            query = "SELECT MAX(OrderID) as max_id FROM `order`"
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result[0] is not None:
                order_id = result[0] + 1
            else:
                order_id = 1
            
            # Insert the order
            query = """
            INSERT INTO `order` (OrderID, OrderDate, Cost, Customer_CustomerID)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (order_id, current_date, str(order_total), customer_id))
            
            # Commit the transaction
            connection.commit()
            
            return order_id
            
        except Error as e:
            print(f"Error creating order: {e}")
            if connection:
                connection.rollback()
            return None
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def process_order_items(self, order_id, customer_id):
        """Process all items in the cart and update the database"""
        connection = self.connect_to_mysql()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Collect all products and their quantities as we did for stock checking
            product_quantities = {}
            self.collect_product_quantities(self.cart_treestore, None, product_quantities)
            
            # Track bundles separately
            bundles = []
            
            # Process top-level items
            for i in range(self.cart_treestore.iter_n_children(None)):
                top_iter = self.cart_treestore.iter_nth_child(None, i)
                item_name = self.cart_treestore.get_value(top_iter, 0)
                item_type = self.cart_treestore.get_value(top_iter, 4)
                
                if item_type == "bundle" or item_type.startswith("bundle-"):
                    # Get the bundle ID - first query it from the database based on name
                    query = "SELECT BundleID FROM bundle WHERE Name = %s"
                    cursor.execute(query, (item_name,))
                    result = cursor.fetchone()
                    
                    if result and result[0] is not None:
                        bundle_id = result[0]
                        bundles.append(bundle_id)
                        
                        # Add the bundle to order_has_bundle
                        query = """
                        INSERT INTO order_has_bundle (Order_OrderID, Order_Customer_CustomerID, Bundle_BundleID)
                        VALUES (%s, %s, %s)
                        """
                        cursor.execute(query, (order_id, customer_id, bundle_id))
            
            # Add all standalone products to order_has_product
            for i in range(self.cart_treestore.iter_n_children(None)):
                top_iter = self.cart_treestore.iter_nth_child(None, i)
                item_name = self.cart_treestore.get_value(top_iter, 0)
                item_type = self.cart_treestore.get_value(top_iter, 4)
                
                if item_type == "product":
                    query = """
                    INSERT INTO order_has_product (Order_OrderID, Order_Customer_CustomerID, Product_Name)
                    VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, (order_id, customer_id, item_name))
            
            # Update product stock for all products
            for product_name, quantity in product_quantities.items():
                # Get current stock
                query = "SELECT Stock FROM product WHERE Name = %s"
                cursor.execute(query, (product_name,))
                result = cursor.fetchone()
                
                if result and result[0] is not None:
                    try:
                        current_stock = int(result[0])
                        new_stock = current_stock - quantity
                        
                        # Update the stock
                        query = "UPDATE product SET Stock = %s WHERE Name = %s"
                        cursor.execute(query, (str(new_stock), product_name))
                    except (ValueError, TypeError):
                        # Handle invalid stock values
                        print(f"Warning: Invalid stock value for {product_name}")
            
            # Commit the transaction
            connection.commit()
            
            return True
            
        except Error as e:
            print(f"Error processing order items: {e}")
            if connection:
                connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_order(self, order_id, customer_id):
        """Delete an order if processing failed"""
        connection = self.connect_to_mysql()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Delete from order_has_bundle
            query = "DELETE FROM order_has_bundle WHERE Order_OrderID = %s AND Order_Customer_CustomerID = %s"
            cursor.execute(query, (order_id, customer_id))
            
            # Delete from order_has_product
            query = "DELETE FROM order_has_product WHERE Order_OrderID = %s AND Order_Customer_CustomerID = %s"
            cursor.execute(query, (order_id, customer_id))
            
            # Delete the order
            query = "DELETE FROM `order` WHERE OrderID = %s AND Customer_CustomerID = %s"
            cursor.execute(query, (order_id, customer_id))
            
            # Commit the transaction
            connection.commit()
            
        except Error as e:
            print(f"Error deleting order: {e}")
            if connection:
                connection.rollback()
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def show_success_dialog(self, message):
        """Show a success dialog with the given message"""
        dialog = Gtk.MessageDialog(
            transient_for=self.addCustomer_window or self.customerManagement_window or self.manager_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

    def on_remove_button_clicked(self, button):
        """Handle click on the remove button"""
        # Get the selection from the cart tree
        selection = self.cart_tree.get_selection()
        model, treeiter = selection.get_selected()
        
        if treeiter is None:
            self.show_error_dialog("Please select an item to remove")
            return
        
        # Get information about the selected item
        item_name = model.get_value(treeiter, 0)
        item_type = model.get_value(treeiter, 4) if model.get_n_columns() > 4 else ""
        
        # Check if this is a product inside a bundle
        parent_iter = model.iter_parent(treeiter)
        if parent_iter is not None:
            # This is a product inside a bundle
            self.show_error_dialog("Cannot remove individual products from a bundle. Remove the entire bundle instead.")
            return
        
        # For a regular product or an entire bundle, confirm before removing
        confirmation_dialog = Gtk.MessageDialog(
            transient_for=self.cart_window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Remove {item_name} from cart?"
        )
        
        if item_type == "bundle":
            confirmation_dialog.format_secondary_text("This will remove the entire bundle and all its products.")
        
        response = confirmation_dialog.run()
        confirmation_dialog.destroy()
        
        if response == Gtk.ResponseType.YES:
            # Remove the item (and all its children if it's a bundle)
            model.remove(treeiter)
            
            # Update the grand total
            self.update_grand_total()


    def get_widget_references(self):
        """Get references to all widgets needed"""
        # Cart window widgets
        self.cart_tree = self.builder.get_object("cart_tree")
        if not self.cart_tree:
            print("Error: Could not find TreeView with ID 'cart_tree'")
            
        self.grand_total_label = self.builder.get_object("grand_total_amount")
        if not self.grand_total_label:
            print("Error: Could not find Label with ID 'grand_total_amount'")
        
        # Browse window widgets
        self.treeview = self.builder.get_object("browse_tree")
        if not self.treeview:
            print("Error: Could not find TreeView with ID 'browse_tree'")
            
        self.search_entry = self.builder.get_object("browse_search")
        if not self.search_entry:
            print("Error: Could not find SearchEntry with ID 'browse_search'")
            
        self.quantity_selector = self.builder.get_object("quantity_selector")
        if not self.quantity_selector:
            print("Error: Could not find SpinButton with ID 'quantity_selector'")
            
        self.add_to_cart_button = self.builder.get_object("addToCart_button")
        if not self.add_to_cart_button:
            print("Error: Could not find Button with ID 'addToCart_button'")
        else:
            self.add_to_cart_button.connect("clicked", self.on_add_to_cart_clicked)

        # My Orders window widgets
        self.my_orders_tree = self.builder.get_object("myOrders_tree")
        if not self.my_orders_tree:
            print("Error: Could not find TreeView with ID 'myOrders_tree'")
        
        # Connect my orders button
        self.my_orders_button = self.builder.get_object("myOrders_button")
        if not self.my_orders_button:
            print("Error: Could not find Button with ID 'myOrders_button'")
        else:
            self.my_orders_button.connect("clicked", self.on_myOrders_button_clicked)
        
        # Add event handler for my orders window close
        self.my_orders_window = self.builder.get_object("myOrders_window")
        if self.my_orders_window:
            self.my_orders_window.connect("delete-event", self.on_myorders_window_close)
        
        # Orders button in manager window
        self.orders_button = self.builder.get_object("orders_button")
        if not self.orders_button:
            print("Error: Could not find Button with ID 'orders_button'")
        else:
            self.orders_button.connect("clicked", self.on_orders_button_clicked)
        
        # Orders window widgets
        self.orders_window = self.builder.get_object("orders_window")
        if self.orders_window:
            self.orders_window.connect("delete-event", self.on_orders_window_close)
        
        self.orders_tree = self.builder.get_object("orders_tree")
        if not self.orders_tree:
            print("Error: Could not find TreeView with ID 'orders_tree'")

        # Manager window widgets
        self.warranty_button = self.builder.get_object("warranty_button")
        if not self.warranty_button:
            print("Error: Could not find Button with ID 'warranty_button'")
        else:
            self.warranty_button.connect("clicked", self.on_warranty_button_clicked)
        
        # Warranty window widgets
        self.warranty_window = self.builder.get_object("warranty_window")
        if self.warranty_window:
            self.warranty_window.connect("delete-event", self.on_warranty_window_close)
        
        self.warranty_tree = self.builder.get_object("warranty_tree")
        if not self.warranty_tree:
            print("Error: Could not find TreeView with ID 'warranty_tree'")

        # Customer Management button in manager window
        self.customerManagement_button = self.builder.get_object("customerManagement_button")
        if not self.customerManagement_button:
            print("Error: Could not find Button with ID 'customerManagement_button'")
        else:
            self.customerManagement_button.connect("clicked", self.on_customerManagement_button_clicked)
        
        # Customer Management window widgets
        self.customerManagement_window = self.builder.get_object("customerManagement_window")
        if self.customerManagement_window:
            self.customerManagement_window.connect("delete-event", self.on_customerManagement_window_close)
        
        self.customers_tree = self.builder.get_object("customers_tree")  # Assuming there's a TreeView to show customers
        if not self.customers_tree:
            print("Error: Could not find TreeView with ID 'customers_tree'")
        
        # Add Customer button in customer management window
        self.addCustomer_button = self.builder.get_object("addCustomer_button")
        if not self.addCustomer_button:
            print("Error: Could not find Button with ID 'addCustomer_button'")
        else:
            self.addCustomer_button.connect("clicked", self.on_addCustomer_button_clicked)
        
        # Add Customer window widgets
        self.addCustomer_window = self.builder.get_object("addCustomer_window")
        if self.addCustomer_window:
            self.addCustomer_window.connect("delete-event", self.on_addCustomer_window_close)
        
        # Get reference to customer input fields in add customer window
        self.customerName_entry = self.builder.get_object("customerName_entry")
        self.customerPhone_entry = self.builder.get_object("customerPhone_entry")
        self.customerEmail_entry = self.builder.get_object("customerEmail_entry")
        self.customerAddress_entry = self.builder.get_object("customerAddress_entry")
        
        # Save new customer button
        self.saveCustomer_button = self.builder.get_object("saveCustomer_button")
        if self.saveCustomer_button:
            self.saveCustomer_button.connect("clicked", self.on_saveCustomer_button_clicked)
        
        # Stock button in manager window
        self.stock_button = self.builder.get_object("stock_button")
        if not self.stock_button:
            print("Error: Could not find Button with ID 'stock_button'")
        else:
            self.stock_button.connect("clicked", self.on_stock_button_clicked)
        
        # Stock window widgets
        self.stock_window = self.builder.get_object("stock_window")
        if self.stock_window:
            self.stock_window.connect("delete-event", self.on_stock_window_close)
        
        self.stock_tree = self.builder.get_object("stock_tree")  # Assuming there's a TreeView to show products
        if not self.stock_tree:
            print("Error: Could not find TreeView with ID 'stock_tree'")
        
        # Add Product button in stock window
        self.addProduct_button = self.builder.get_object("addProduct_button")
        if not self.addProduct_button:
            print("Error: Could not find Button with ID 'addProduct_button'")
        else:
            self.addProduct_button.connect("clicked", self.on_addProduct_button_clicked)
        
        # Add Product window widgets
        self.addProduct_window = self.builder.get_object("addProduct_window")
        if self.addProduct_window:
            self.addProduct_window.connect("delete-event", self.on_addProduct_window_close)
        
        # Get reference to product input fields in add product window
        self.productName_entry = self.builder.get_object("productName_entry")
        self.productPrice_entry = self.builder.get_object("productPrice_entry")
        self.productStock_entry = self.builder.get_object("productStock_entry")
        
        # Save new product button
        self.saveProduct_button = self.builder.get_object("saveProduct_button")
        if self.saveProduct_button:
            self.saveProduct_button.connect("clicked", self.on_saveProduct_button_clicked)
        
        # Stock search entry
        self.stock_search = self.builder.get_object("stock_search")
        if not self.stock_search:
            print("Error: Could not find SearchEntry with ID 'stock_search'")
        else:
            self.stock_search.connect("search-changed", self.on_stock_search_changed)
        
        # Stock quantity spinner
        self.stock_quantity = self.builder.get_object("stock_quantity")
        if not self.stock_quantity:
            print("Error: Could not find SpinButton with ID 'stock_quantity'")
        else:
            self.configure_stock_quantity_spinner()
        
        # Add Stock button
        self.addStock_button = self.builder.get_object("addStock_button")
        if not self.addStock_button:
            print("Error: Could not find Button with ID 'addStock_button'")
        else:
            self.addStock_button.connect("clicked", self.on_addStock_button_clicked)
            # Initially disable the button until a product is selected
            self.addStock_button.set_sensitive(False)
        # Manage Bundles button in stock window
        self.manageBundles_button = self.builder.get_object("manageBundles_button")
        if not self.manageBundles_button:
            print("Error: Could not find Button with ID 'manageBundles_button'")
        else:
            self.manageBundles_button.connect("clicked", self.on_manageBundles_button_clicked)
        
        # Bundle window widgets
        self.bundle_window = self.builder.get_object("bundle_window")
        if self.bundle_window:
            self.bundle_window.connect("delete-event", self.on_bundle_window_close)
        
        self.bundle_tree = self.builder.get_object("bundle_tree")
        if not self.bundle_tree:
            print("Error: Could not find TreeView with ID 'bundle_tree'")
        
        # Remove Bundle button
        self.removeBundle_button = self.builder.get_object("removeBundle_button")
        if not self.removeBundle_button:
            print("Error: Could not find Button with ID 'removeBundle_button'")
        else:
            self.removeBundle_button.connect("clicked", self.on_removeBundle_button_clicked)
            # Initially disable the button until a bundle is selected
            self.removeBundle_button.set_sensitive(False)
        
            # New Bundle button
            self.newBundle_button = self.builder.get_object("newBundle_button")
            if not self.newBundle_button:
                print("Error: Could not find Button with ID 'newBundle_button'")
            else:
                self.newBundle_button.connect("clicked", self.on_newBundle_button_clicked)
            
            # Bundle Maker window widgets
            self.bundleMaker_window = self.builder.get_object("bundleMaker_window")
            if self.bundleMaker_window:
                self.bundleMaker_window.connect("delete-event", self.on_bundleMaker_window_close)
            
            self.bundleProducts_tree = self.builder.get_object("bundleProducts_tree")
            if not self.bundleProducts_tree:
                print("Error: Could not find TreeView with ID 'bundleProducts_tree'")
            
            self.bundleName_entry = self.builder.get_object("bundleName_entry")
            self.bundleDiscount_entry = self.builder.get_object("bundleDiscount_entry")
            
            # Save Bundle button
            self.saveBundle_button = self.builder.get_object("saveBundle_button")
            if not self.saveBundle_button:
                print("Error: Could not find Button with ID 'saveBundle_button'")
            else:
                self.saveBundle_button.connect("clicked", self.on_saveBundle_button_clicked)
    

    def on_myorders_window_close(self, window, event):
        """Handle my orders window close event"""
        # Hide the my orders window and show the customer window
        self.my_orders_window.hide()
        self.customer_window.show_all()
        
        # Return True to prevent the default handler from being called
        return True
    
    def setup_myorders_treeview(self):
        """Set up the my orders TreeView with columns"""
        if not self.my_orders_tree:
            return
            
        # Create a ListStore for orders with columns:
        # [OrderID (int), OrderDate (str), Total Cost (float), Items Count (int)]
        self.myorders_liststore = Gtk.ListStore(int, str, float, int)
        self.my_orders_tree.set_model(self.myorders_liststore)
        
        # Remove any existing columns
        for column in self.my_orders_tree.get_columns():
            self.my_orders_tree.remove_column(column)
        
        # Add columns for the orders
        columns = [
            ("Order ID", 100, 0, int),
            ("Date", 150, 1, str),
            ("Total", 100, 2, float, self.price_cell_data_func),
            ("Items", 80, 3, int)
        ]
        
        for i, (title, width, index, data_type, *args) in enumerate(columns):
            renderer = Gtk.CellRendererText()
            
            if args and args[0]:  # If a custom formatter is provided
                column = Gtk.TreeViewColumn(title, renderer)
                column.set_cell_data_func(renderer, args[0])
            else:
                column = Gtk.TreeViewColumn(title, renderer, text=index)
                    
            column.set_resizable(True)
            column.set_min_width(width)
            column.set_sort_column_id(index)
            self.my_orders_tree.append_column(column)

        self.my_orders_tree.connect("row-activated", self.on_order_row_activated)
        
        # Add selection handling
        ##selection = self.my_orders_tree.get_selection()
        ##selection.set_mode(Gtk.SelectionMode.SINGLE)
        ##selection.connect("changed", self.on_order_selection_changed)
    
    def on_order_row_activated(self, treeview, path, column):
        """Handle double-click on order row"""
        model = treeview.get_model()
        iter = model.get_iter(path)
        
        if iter:
            # Get the selected order ID
            order_id = model.get_value(iter, 0)
            
            # Load and display order details
            self.load_order_details(order_id, self.customer_id)

    def load_order_details(self, order_id, customer_id):
        """Load and display details for a specific order"""
        # You could create another TreeView to show order details,
        # or use labels to display the information.
        
        connection = self.connect_to_mysql()
        if not connection:
            return
            
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get products in the order
            query1 = """
            SELECT p.Name, p.Price
            FROM product p
            JOIN order_has_product ohp ON p.Name = ohp.Product_Name
            WHERE ohp.Order_OrderID = %s AND ohp.Order_Customer_CustomerID = %s
            """
            cursor.execute(query1, (order_id, customer_id))
            products = cursor.fetchall()
            
            # Get bundles in the order
            query2 = """
            SELECT b.Name, b.Discount
            FROM bundle b
            JOIN order_has_bundle ohb ON b.BundleID = ohb.Bundle_BundleID
            WHERE ohb.Order_OrderID = %s AND ohb.Order_Customer_CustomerID = %s
            """
            cursor.execute(query2, (order_id, customer_id))
            bundles = cursor.fetchall()
            
            # Display the details in your UI
            # For example, display in a message dialog
            details = f"Order #{order_id} Details:\n\n"
            
            details += "Products:\n"
            for product in products:
                details += f"- {product['Name']}: ${float(product['Price']):.2f}\n"
            
            details += "\nBundles:\n"
            for bundle in bundles:
                details += f"- {bundle['Name']} (Discount: {bundle['Discount']}%)\n"
            
            # Show the details
            self.show_info_dialog(details)
            
        except Error as e:
            print(f"Error loading order details: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def show_info_dialog(self, message):
        """Show an information dialog with the given message"""
        dialog = Gtk.MessageDialog(
            transient_for=self.warranty_window or self.manager_window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

    def load_customer_orders(self, customer_id):
        """Load orders for a specific customer"""
        connection = self.connect_to_mysql()
        if not connection:
            return
            
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query to get all orders for this customer
            query = """
            SELECT o.OrderID, o.OrderDate, o.Cost 
            FROM `order` o
            WHERE o.Customer_CustomerID = %s
            ORDER BY o.OrderDate DESC
            """
            cursor.execute(query, (customer_id,))
            orders = cursor.fetchall()
            
            # Clear existing data
            self.myorders_liststore.clear()
            
            # Add each order to the list
            for order in orders:
                order_id = order['OrderID']
                order_date = order['OrderDate']
                order_cost = float(order['Cost']) if order['Cost'] is not None else 0.0
                
                # Count the number of items in this order
                items_count = self.count_order_items(cursor, order_id, customer_id)
                
                # Add to ListStore
                self.myorders_liststore.append([
                    order_id,
                    order_date,
                    order_cost,
                    items_count
                ])
                
        except Error as e:
            print(f"Error loading orders: {e}")
            self.show_error_dialog(f"Error loading orders: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_bundle_window_close(self, window, event):
        """Handle bundle window close event"""
        # Hide bundle window and show stock window
        self.bundle_window.hide()
        self.stock_window.show_all()
        
        # Return True to prevent the default handler from being called
        return True

    def on_removeBundle_button_clicked(self, button):
        """Handle click on remove bundle button"""
        # Get the selected bundle
        selection = self.bundle_tree.get_selection()
        model, iter = selection.get_selected()
        
        if not iter:
            self.show_error_dialog("Please select a bundle to remove.")
            return
        
        # Get the bundle info
        bundle_id = model.get_value(iter, 0)
        bundle_name = model.get_value(iter, 1)
        
        # Confirm deletion
        confirmation = Gtk.MessageDialog(
            transient_for=self.bundle_window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Are you sure you want to remove the bundle '{bundle_name}'?"
        )
        confirmation.format_secondary_text("This action cannot be undone.")
        
        response = confirmation.run()
        confirmation.destroy()
        
        if response == Gtk.ResponseType.YES:
            # Remove the bundle
            success = self.remove_bundle(bundle_id)
            
            if success:
                # Remove from the liststore
                model.remove(iter)
                
                # Show success message
                self.show_success_dialog(f"Bundle '{bundle_name}' has been removed.")
            else:
                # Error message is shown in remove_bundle method
                pass

    def on_newBundle_button_clicked(self, button):
        """Handle click on new bundle button"""
        # Clear any previous input
        if self.bundleName_entry:
            self.bundleName_entry.set_text("")
        if self.bundleDiscount_entry:
            self.bundleDiscount_entry.set_text("")
        
        # Load products for bundle maker
        self.load_products_for_bundle()
        
        # Hide bundle window
        self.bundle_window.hide()
        
        # Show bundle maker window
        if self.bundleMaker_window:
            self.bundleMaker_window.show_all()
        else:
            self.show_error_dialog("Bundle Maker window not found.")
            # Show bundle window again if bundle maker window doesn't exist
            self.bundle_window.show_all()

    def on_bundleMaker_window_close(self, window, event):
        """Handle bundle maker window close event"""
        # Hide bundle maker window and show bundle window
        self.bundleMaker_window.hide()
        self.bundle_window.show_all()
        
        # Return True to prevent the default handler from being called
        return True

    def on_saveBundle_button_clicked(self, button):
        """Handle click on save bundle button"""
        # Get bundle information
        name = self.bundleName_entry.get_text().strip() if self.bundleName_entry else ""
        discount_text = self.bundleDiscount_entry.get_text().strip() if self.bundleDiscount_entry else ""
        
        # Validate input
        if not name:
            self.show_error_dialog("Bundle name is required.")
            return
        
        # Validate discount
        try:
            discount = float(discount_text)
            if discount < 0 or discount > 100:
                self.show_error_dialog("Discount must be between 0 and 100.")
                return
        except ValueError:
            self.show_error_dialog("Discount must be a valid number.")
            return
        
        # Get selected products
        selected_products = self.get_selected_products_for_bundle()
        
        if not selected_products:
            self.show_error_dialog("Please select at least one product for the bundle.")
            return
        
        # Save the new bundle
        success = self.create_new_bundle(name, discount, selected_products)
        
        if success:
            # Show success message
            self.show_success_dialog(f"Bundle '{name}' has been created successfully.")
            
            # Close bundle maker window and return to bundle management
            self.bundleMaker_window.hide()
            
            # Refresh the bundle list
            self.load_bundles_for_management()
            
            # Show bundle window
            self.bundle_window.show_all()
        else:
            # Error message is shown in create_new_bundle method
            pass

    def setup_bundle_treeview(self):
        """Set up the bundle TreeView with columns"""
        if not self.bundle_tree:
            return
        
        # Create a ListStore for bundles with columns:
        # [BundleID (int), Name (str), Discount (str), Num Products (int)]
        self.bundle_liststore = Gtk.ListStore(int, str, str, int)
        self.bundle_tree.set_model(self.bundle_liststore)
        
        # Remove any existing columns
        for column in self.bundle_tree.get_columns():
            self.bundle_tree.remove_column(column)
        
        # Add columns for bundles
        columns = [
            ("ID", 80, 0, int),
            ("Bundle Name", 250, 1, str),
            ("Discount", 100, 2, str),
            ("# Products", 100, 3, int)
        ]
        
        for i, (title, width, index, data_type) in enumerate(columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=index)
            column.set_resizable(True)
            column.set_min_width(width)
            column.set_sort_column_id(index)
            self.bundle_tree.append_column(column)
        
        # Connect row-activated signal for bundle details
        self.bundle_tree.connect("row-activated", self.on_bundle_row_activated)
        
        # Add selection handling to update remove bundle button sensitivity
        selection = self.bundle_tree.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        selection.connect("changed", self.on_bundle_selection_changed)

    def setup_bundle_products_treeview(self):
        """Set up the bundle products TreeView with columns and selection"""
        if not self.bundleProducts_tree:
            return
        
        # Create a ListStore for products with columns:
        # [Name (str), Price (float), Selected (bool)]
        self.bundle_products_liststore = Gtk.ListStore(str, float, bool)
        self.bundleProducts_tree.set_model(self.bundle_products_liststore)
        
        # Remove any existing columns
        for column in self.bundleProducts_tree.get_columns():
            self.bundleProducts_tree.remove_column(column)
        
        # Add toggle column for selection
        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_product_toggled)
        column_toggle = Gtk.TreeViewColumn("Select", renderer_toggle, active=2)
        column_toggle.set_resizable(True)
        column_toggle.set_min_width(60)
        self.bundleProducts_tree.append_column(column_toggle)
        
        # Add product info columns
        columns = [
            ("Product Name", 250, 0, str),
            ("Price", 100, 1, float, self.price_cell_data_func)
        ]
        
        for i, (title, width, index, data_type, *args) in enumerate(columns):
            renderer = Gtk.CellRendererText()
            
            if args and args[0]:  # If a custom formatter is provided
                column = Gtk.TreeViewColumn(title, renderer)
                column.set_cell_data_func(renderer, args[0])
            else:
                column = Gtk.TreeViewColumn(title, renderer, text=index)
                
            column.set_resizable(True)
            column.set_min_width(width)
            column.set_sort_column_id(index)
            self.bundleProducts_tree.append_column(column)

    def on_product_toggled(self, cell, path):
        """Handle toggling of product selection"""
        # Toggle the selection state
        self.bundle_products_liststore[path][2] = not self.bundle_products_liststore[path][2]

    def on_bundle_selection_changed(self, selection):
        """Handle selection change in bundle tree"""
        model, iter = selection.get_selected()
        
        # Enable or disable remove bundle button based on selection
        if self.removeBundle_button:
            self.removeBundle_button.set_sensitive(iter is not None)

    def load_bundles_for_management(self):
        """Load all bundles for the bundle management window"""
        connection = self.connect_to_mysql()
        if not connection:
            return
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query to get all bundles
            query = "SELECT BundleID, Name, Discount FROM bundle ORDER BY Name"
            cursor.execute(query)
            bundles = cursor.fetchall()
            
            # Clear existing data
            self.bundle_liststore.clear()
            
            # Add each bundle to the list
            for bundle in bundles:
                bundle_id = bundle['BundleID']
                bundle_name = bundle['Name']
                discount = bundle['Discount']
                
                # Format discount with % sign
                formatted_discount = f"{discount}%" if discount else "0%"
                
                # Count products in the bundle
                products_query = """
                SELECT COUNT(*) as count
                FROM bundle_has_product
                WHERE Bundle_BundleID = %s
                """
                cursor.execute(products_query, (bundle_id,))
                count_result = cursor.fetchone()
                product_count = count_result['count'] if count_result else 0
                
                self.bundle_liststore.append([
                    bundle_id,
                    bundle_name,
                    formatted_discount,  # Now includes the % sign
                    product_count
                ])
                
        except Error as e:
            print(f"Error loading bundles: {e}")
            self.show_error_dialog(f"Error loading bundles: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def load_products_for_bundle(self):
        """Load all products for the bundle maker"""
        connection = self.connect_to_mysql()
        if not connection:
            return
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Query to get all products
            query = "SELECT Name, Price FROM product ORDER BY Name"
            cursor.execute(query)
            products = cursor.fetchall()
            
            # Clear existing data
            self.bundle_products_liststore.clear()
            
            # Add each product to the list (initially unselected)
            for product in products:
                try:
                    name = product['Name']
                    price = float(product['Price']) if product['Price'] is not None else 0.0
                    
                    self.bundle_products_liststore.append([
                        name,
                        price,
                        False  # Initially unselected
                    ])
                except (ValueError, TypeError) as e:
                    print(f"Error processing product {product['Name']}: {e}")
                
        except Error as e:
            print(f"Error loading products: {e}")
            self.show_error_dialog(f"Error loading products: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_selected_products_for_bundle(self):
        """Get list of selected products for the new bundle"""
        selected_products = []
        
        # Iterate through the liststore and find selected products
        for row in self.bundle_products_liststore:
            if row[2]:  # If selected
                selected_products.append(row[0])  # Add product name
        
        return selected_products

    def create_new_bundle(self, name, discount, products):
        """Create a new bundle with the given products"""
        connection = self.connect_to_mysql()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Check if bundle with this name already exists
            query = "SELECT 1 FROM bundle WHERE Name = %s"
            cursor.execute(query, (name,))
            
            if cursor.fetchone():
                self.show_error_dialog(f"A bundle with the name '{name}' already exists.")
                return False
            
            # Insert the new bundle
            query = """
            INSERT INTO bundle (Name, Discount)
            VALUES (%s, %s)
            """
            cursor.execute(query, (name, str(discount)))
            
            # Get the auto-generated bundle ID
            bundle_id = cursor.lastrowid
            
            # Add products to the bundle
            for product_name in products:
                query = """
                INSERT INTO bundle_has_product (Bundle_BundleID, Product_Name)
                VALUES (%s, %s)
                """
                cursor.execute(query, (bundle_id, product_name))
            
            # Commit the transaction
            connection.commit()
            
            return True
            
        except Error as e:
            print(f"Error creating bundle: {e}")
            self.show_error_dialog(f"Error creating bundle: {e}")
            if connection:
                connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def remove_bundle(self, bundle_id):
        """Remove a bundle and its product associations"""
        connection = self.connect_to_mysql()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # First delete from bundle_has_product (foreign key constraint)
            query1 = "DELETE FROM bundle_has_product WHERE Bundle_BundleID = %s"
            cursor.execute(query1, (bundle_id,))
            
            # Check if the bundle has a warranty associated with it
            query_warranty = "SELECT 1 FROM warranty WHERE Bundle_BundleID = %s"
            cursor.execute(query_warranty, (bundle_id,))
            
            if cursor.fetchone():
                # Delete from warranty
                query_delete_warranty = "DELETE FROM warranty WHERE Bundle_BundleID = %s"
                cursor.execute(query_delete_warranty, (bundle_id,))
            
            # Then delete the bundle
            query2 = "DELETE FROM bundle WHERE BundleID = %s"
            cursor.execute(query2, (bundle_id,))
            
            # Commit the transaction
            connection.commit()
            
            # Check if the deletion was successful
            if cursor.rowcount > 0:
                return True
            else:
                self.show_error_dialog(f"Bundle with ID {bundle_id} not found.")
                return False
            
        except Error as e:
            print(f"Error removing bundle: {e}")
            self.show_error_dialog(f"Error removing bundle: {e}")
            if connection:
                connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def on_bundle_row_activated(self, treeview, path, column):
        """Handle double-click on bundle row"""
        model = treeview.get_model()
        iter = model.get_iter(path)
        
        if iter:
            # Get the selected bundle details
            bundle_id = model.get_value(iter, 0)
            bundle_name = model.get_value(iter, 1)
            discount = model.get_value(iter, 2)
            
            # Load bundle products
            self.show_bundle_details(bundle_id, bundle_name, discount)

    def show_bundle_details(self, bundle_id, bundle_name, discount):
        """Show details of a bundle including its products"""
        connection = self.connect_to_mysql()
        if not connection:
            return
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Get products in the bundle
            query = """
            SELECT p.Name, p.Price
            FROM product p
            JOIN bundle_has_product bhp ON p.Name = bhp.Product_Name
            WHERE bhp.Bundle_BundleID = %s
            ORDER BY p.Name
            """
            cursor.execute(query, (bundle_id,))
            products = cursor.fetchall()
            
            # Calculate total price and discounted price
            total_price = 0.0
            for product in products:
                price = float(product['Price']) if product['Price'] is not None else 0.0
                total_price += price
            
            try:
                discount_value = float(discount) if discount else 0
                discounted_price = total_price * (1 - discount_value / 100)
            except ValueError:
                discount_value = 0
                discounted_price = total_price
            
            # Format details for display
            details = f"Bundle Details: {bundle_name}\n\n"
            details += f"Discount: {discount}%\n"
            details += f"Original Price: ${total_price:.2f}\n"
            details += f"Discounted Price: ${discounted_price:.2f}\n"
            details += f"Savings: ${(total_price - discounted_price):.2f}\n\n"
            
            details += f"Products in this bundle:\n"
            for product in products:
                price = float(product['Price']) if product['Price'] is not None else 0.0
                details += f"- {product['Name']}: ${price:.2f}\n"
            
            # Show the details
            self.show_info_dialog(details)
            
        except Error as e:
            print(f"Error loading bundle details: {e}")
            self.show_error_dialog(f"Error loading bundle details: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def count_order_items(self, cursor, order_id, customer_id):
        """Count the number of products and bundles in an order"""
        try:
            # Count products
            query1 = """
            SELECT COUNT(*) as count
            FROM order_has_product
            WHERE Order_OrderID = %s AND Order_Customer_CustomerID = %s
            """
            cursor.execute(query1, (order_id, customer_id))
            product_count = cursor.fetchone()['count']
            
            # Count bundles
            query2 = """
            SELECT COUNT(*) as count
            FROM order_has_bundle
            WHERE Order_OrderID = %s AND Order_Customer_CustomerID = %s
            """
            cursor.execute(query2, (order_id, customer_id))
            bundle_count = cursor.fetchone()['count']
            
            return product_count + bundle_count
            
        except Error as e:
            print(f"Error counting order items: {e}")
            return 0

    def on_browse_button_clicked(self, button):
        """Handle click on the browse button"""
        if not self.browse_window:
            return
            
        # Load product data if we haven't already
        if not hasattr(self, 'data_loaded') or not self.data_loaded:
            self.load_data_from_mysql()
            self.setup_search()
            self.data_loaded = True
        
        # Show the browse window
        self.browse_window.show_all()
    
    def on_browse_window_close(self, window, event):
        """Handle browse window close event"""
        # Hide the window instead of destroying it
        window.hide()
        # Return True to prevent the default handler from being called
        return True
    
    def configure_quantity_spinner(self):
        """Configure the quantity spinner with proper settings"""
        if not self.quantity_selector:
            return
            
        # Set the range (minimum, maximum)
        self.quantity_selector.set_range(1, 100)  # Allow values from 1 to 100
        
        # Set the default value
        self.quantity_selector.set_value(1)
        
        # Set the step increment (how much it changes when +/- is clicked)
        self.quantity_selector.set_increments(1, 10)  # Small step 1, large step 10
        
        # Make sure it's editable
        self.quantity_selector.set_editable(True)
        
        # Set numeric mode
        self.quantity_selector.set_numeric(True)
        
        # Update the policy to update the value when changed
        self.quantity_selector.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
    
    def setup_treeview(self):
        """Set up the TreeView with columns and a TreeStore model"""
        if not self.treeview:
            return
            
        # Create a TreeStore model with the appropriate data types
        # We'll also add a 4th column for the original price (not displayed)
        # and a 5th column for an ID or type flag (bundle ID or "product")
        model_types = [attr[3] for attr in self.attributes_to_display]
        model_types.extend([float, str])  # Original price and item type
        self.treestore = Gtk.TreeStore(*model_types)
        self.treeview.set_model(self.treestore)
        
        # Remove any existing columns
        for column in self.treeview.get_columns():
            self.treeview.remove_column(column)
        
        # Add columns for each attribute
        for i, (column_name, title, width, data_type) in enumerate(self.attributes_to_display):
            self.add_column_to_treeview(i, column_name, title, width, data_type)
        
        # Make the TreeView expandable
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_show_expanders(True)
    
    def setup_cart_treeview(self):
        """Set up the cart TreeView with columns"""
        if not self.cart_tree:
            return
            
        # Create a TreeStore for the cart with columns:
        # [Name (str), Price (float), Quantity (int), Total (float), Type (str), Parent (str)]
        # Type will be "bundle", "bundle-product", or "product"
        # Parent will be the bundle name for bundle products, or empty for standalone items
        self.cart_treestore = Gtk.TreeStore(str, float, int, float, str, str)
        
        # Connect to the row-changed, row-inserted, and row-deleted signals
        self.cart_treestore.connect("row-changed", self.on_cart_changed)
        self.cart_treestore.connect("row-inserted", self.on_cart_changed)
        self.cart_treestore.connect("row-deleted", self.on_cart_changed)
        
        self.cart_tree.set_model(self.cart_treestore)
        
        # Remove any existing columns
        for column in self.cart_tree.get_columns():
            self.cart_tree.remove_column(column)
        
        # Add columns for the cart
        columns = [
            ("Product", 200, 0, str),
            ("Price", 100, 1, float, self.price_cell_data_func),
            ("Quantity", 80, 2, int, None, True),  # Added True for editable
            ("Total", 100, 3, float, self.total_cell_data_func)
        ]
        
        for i, (title, width, index, data_type, *args) in enumerate(columns):
            renderer = Gtk.CellRendererText()
            
            # If this is the quantity column and it should be editable
            if args and len(args) > 1 and args[1]:
                renderer.set_property("editable", True)
                renderer.connect("edited", self.on_cart_quantity_edited, index)
            
            if args and len(args) > 0 and args[0]:  # If a custom formatter is provided
                column = Gtk.TreeViewColumn(title, renderer)
                column.set_cell_data_func(renderer, args[0])
            else:
                column = Gtk.TreeViewColumn(title, renderer, text=index)
                    
            column.set_resizable(True)
            column.set_min_width(width)
            column.set_sort_column_id(index)
            self.cart_tree.append_column(column)
        
        # Make the TreeView expandable
        self.cart_tree.set_enable_tree_lines(True)
        self.cart_tree.set_show_expanders(True)

        # Add row selection handling to update remove button sensitivity
        selection = self.cart_tree.get_selection()
        selection.set_mode(Gtk.SelectionMode.SINGLE)
        selection.connect("changed", self.on_cart_selection_changed)
        
    def on_cart_selection_changed(self, selection):
        """Update the remove button sensitivity based on selection"""
        if not hasattr(self, 'remove_button') or not self.remove_button:
            return
            
        model, treeiter = selection.get_selected()
        
        if treeiter is None:
            # No selection, disable the remove button
            self.remove_button.set_sensitive(False)
            return
        
        # Check if this is a product inside a bundle
        parent_iter = model.iter_parent(treeiter)
        if parent_iter is not None:
            # This is a product inside a bundle - disable the remove button
            self.remove_button.set_sensitive(False)
            
            # Optionally set a tooltip explaining why
            self.remove_button.set_tooltip_text("Cannot remove individual products from a bundle")
        else:
            # This is a top-level item (product or bundle) - enable the remove button
            self.remove_button.set_sensitive(True)
            self.remove_button.set_tooltip_text("Remove the selected item from the cart")
    
    def on_cart_quantity_edited(self, renderer, path, new_text, column):
        """Handle editing of the quantity column in the cart"""
        try:
            # Convert the new text to an integer
            new_quantity = int(new_text)
            
            # Make sure it's a positive number
            if new_quantity <= 0:
                self.show_error_dialog("Quantity must be greater than zero")
                return
            
            # Update the row
            iter = self.cart_treestore.get_iter(path)
            current_price = self.cart_treestore.get_value(iter, 1)
            new_total = current_price * new_quantity
            item_type = self.cart_treestore.get_value(iter, 4)
            
            # Update the quantity and total for this item
            self.cart_treestore.set_value(iter, 2, new_quantity)
            self.cart_treestore.set_value(iter, 3, new_total)
            
            # If this is a bundle, update all child products too
            if item_type == "bundle" and self.cart_treestore.iter_has_child(iter):
                # Calculate the ratio between new and old quantities
                old_quantity = self.cart_treestore.get_value(iter, 2)
                if old_quantity == 0:  # Avoid division by zero
                    ratio = 1
                else:
                    ratio = new_quantity / old_quantity
                    
                # Update each child product
                for i in range(self.cart_treestore.iter_n_children(iter)):
                    child_iter = self.cart_treestore.iter_nth_child(iter, i)
                    
                    child_quantity = self.cart_treestore.get_value(child_iter, 2)
                    child_price = self.cart_treestore.get_value(child_iter, 1)
                    
                    # Update child quantity and total proportionally
                    new_child_quantity = int(child_quantity * ratio)
                    if new_child_quantity < 1:
                        new_child_quantity = 1
                        
                    new_child_total = child_price * new_child_quantity
                    
                    self.cart_treestore.set_value(child_iter, 2, new_child_quantity)
                    self.cart_treestore.set_value(child_iter, 3, new_child_total)
                
        except ValueError:
            self.show_error_dialog("Please enter a valid number")
    
    def on_cart_changed(self, model, path, iter=None):
        """Called whenever the cart model is changed in any way"""
        self.update_grand_total()
    
    def update_grand_total(self):
        """Update the grand total label with the current cart total"""
        if not hasattr(self, 'cart_treestore') or not self.grand_total_label:
            return
        
        grand_total = 0.0
        
        # Only count top-level items (not bundle products) to avoid double counting
        for row in self.cart_treestore:
            # Get the total for this row
            total = row[3]
            grand_total += total
        
        # Format the total with 2 decimal places and $ sign
        formatted_total = f"${grand_total:.2f}"
        
        # Update the label
        self.grand_total_label.set_text(formatted_total)
    
    # The rest of your existing methods (add_column_to_treeview, setup_search, etc.)
    def add_column_to_treeview(self, index, column_name, title, width, data_type):
        """Add a single column to the TreeView"""
        renderer = Gtk.CellRendererText()
        
        # For Price column (float), format with 2 decimal places
        if column_name == "Price" and data_type == float:
            column = Gtk.TreeViewColumn(title, renderer)
            column.set_cell_data_func(renderer, self.price_cell_data_func)
        # For Discount column, show % symbol
        elif column_name == "Discount" and data_type == str:
            column = Gtk.TreeViewColumn(title, renderer)
            column.set_cell_data_func(renderer, self.discount_cell_data_func)
        else:
            column = Gtk.TreeViewColumn(title, renderer, text=index)
            
        column.set_resizable(True)
        column.set_min_width(width)
        column.set_sort_column_id(index)
        self.treeview.append_column(column)
    def discount_cell_data_func(self, column, cell, model, iter, data=None):
        """Custom function to format discount values with % symbol"""
        discount = model.get_value(iter, 1)  # Discount is the second column (index 1)
        
        if discount and discount.strip():
            # Only add % if the discount is not empty
            formatted_discount = f"{discount}%"
            cell.set_property("text", formatted_discount)
        else:
            cell.set_property("text", "")
    
    def price_cell_data_func(self, column, cell, model, iter, data=None):
        """Custom function to format price values with 2 decimal places"""
        # Determine if this is the browse tree or cart tree based on the model structure
        is_cart_model = isinstance(model, Gtk.TreeStore) and model.get_n_columns() >= 5
        
        # Get the price column index based on the model
        price_col = 1 if is_cart_model else 2  # Price is column 1 in cart, column 2 in browse tree
        
        # Get the value, handling filtered models
        if isinstance(model, Gtk.TreeModelFilter):
            # For filtered models, need to get the child iter and model
            child_iter = model.convert_iter_to_child_iter(iter)
            child_model = model.get_model()
            price_value = child_model.get_value(child_iter, price_col)
        else:
            price_value = model.get_value(iter, price_col)
        
        try:
            # Ensure the price is a float and format it
            price_float = float(price_value) if price_value is not None else 0.0
            formatted_price = f"${price_float:.2f}"
        except (ValueError, TypeError) as e:
            # If conversion fails, log error and show default
            print(f"Error formatting price {price_value}: {e}")
            formatted_price = f"${0.00:.2f}"
        
        cell.set_property("text", formatted_price)
    
    def total_cell_data_func(self, column, cell, model, iter, data=None):
        """Custom function to format total values with 2 decimal places"""
        # Total is always column 3 for both models
        total_col = 3
        
        # Get the value, handling filtered models
        if isinstance(model, Gtk.TreeModelFilter):
            child_iter = model.convert_iter_to_child_iter(iter)
            child_model = model.get_model()
            total_value = child_model.get_value(child_iter, total_col)
        else:
            total_value = model.get_value(iter, total_col)
        
        try:
            # Ensure the total is a float and format it
            total_float = float(total_value) if total_value is not None else 0.0
            formatted_total = f"${total_float:.2f}"
        except (ValueError, TypeError) as e:
            print(f"Error formatting total {total_value}: {e}")
            formatted_total = f"${0.00:.2f}"
        
        cell.set_property("text", formatted_total)
    
    def setup_search(self):
        """Set up the search functionality"""
        if not self.search_entry or not self.treeview or not hasattr(self, 'treestore'):
            return
            
        # Connect the search entry's search-changed signal
        self.search_entry.connect("search-changed", self.on_search_changed)
        
        # Create a TreeModelFilter for searching
        self.filter_model = self.treestore.filter_new()
        self.filter_model.set_visible_func(self.filter_visible_func)
        
        # Set the filter model on the TreeView instead of the direct TreeStore
        self.treeview.set_model(self.filter_model)
    
    def filter_visible_func(self, model, iter, data):
        """Filter function that determines which rows to show based on search text"""
        search_text = self.search_entry.get_text().lower()
        
        # If search is empty, show all rows
        if not search_text:
            return True
        
        # First, check if this node matches directly
        value = model.get_value(iter, self.search_attribute_index)
        if value is not None:
            value_str = str(value).lower()
            if search_text in value_str:
                return True
        
        # If this node is a parent, check if any child matches
        if model.iter_has_child(iter):
            for i in range(model.iter_n_children(iter)):
                child = model.iter_nth_child(iter, i)
                child_value = model.get_value(child, self.search_attribute_index)
                if child_value is not None and search_text in str(child_value).lower():
                    return True
        
        # If this node is a child, check if parent matches
        parent = model.iter_parent(iter)
        if parent:
            parent_value = model.get_value(parent, self.search_attribute_index)
            if parent_value is not None and search_text in str(parent_value).lower():
                return True
        
        # No match found
        return False

    def on_search_changed(self, entry):
        """Called when the search text changes"""
        # Refilter the model
        self.filter_model.refilter()
    
    def connect_to_mysql(self):
        """Connect to MySQL database"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            
            if connection.is_connected():
                return connection
                
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.show_error_dialog(f"Database connection error: {e}")
            return None
    
    def load_data_from_mysql(self):
        """Load data from MySQL into the TreeView"""
        if not hasattr(self, 'treestore'):
            print("Error: TreeView not set up properly")
            return
            
        connection = self.connect_to_mysql()
        if not connection:
            return
            
        try:
            cursor = connection.cursor(dictionary=True)  # Get results as dictionaries
            
            # Clear existing data
            self.treestore.clear()
            
            # First, load all bundles
            self.load_bundles(cursor)
            
            # Then, load all products that are not in any bundle
            self.load_standalone_products(cursor)
            
        except Error as e:
            print(f"Error loading data: {e}")
            self.show_error_dialog(f"Error loading data: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def load_bundles(self, cursor):
        """Load all bundles and their products"""
        try:
            # Get all bundles
            query = "SELECT BundleID, Name, Discount FROM bundle"
            cursor.execute(query)
            bundles = cursor.fetchall()
            
            # Process each bundle
            for bundle in bundles:
                bundle_id = bundle['BundleID']
                bundle_name = bundle['Name']
                discount_percent = bundle['Discount']
                
                # Create the bundle as a parent node
                # Format: Name, Discount, Price (will be calculated), Original Price, Type
                bundle_iter = self.treestore.append(None, [bundle_name, discount_percent, 0.0, 0.0, f"bundle-{bundle_id}"])
                
                # Get products in this bundle
                query = """
                SELECT p.Name, p.Price 
                FROM product p
                JOIN bundle_has_product bp ON p.Name = bp.Product_Name
                WHERE bp.Bundle_BundleID = %s
                """
                cursor.execute(query, (bundle_id,))
                products = cursor.fetchall()
                
                # Calculate total price and add products as children
                total_price = 0.0
                for product in products:
                    product_name = product['Name']
                    product_price = float(product['Price']) if product['Price'] is not None else 0.0
                    total_price += product_price
                    
                    # Add product as child of bundle
                    # Child nodes have empty discount, original price, and "product" type
                    self.treestore.append(bundle_iter, [product_name, "", product_price, product_price, "product"])
                
                # Calculate discounted price
                try:
                    discount = float(discount_percent) if discount_percent else 0
                    discounted_price = total_price * (1 - discount / 100)
                except (ValueError, TypeError):
                    discounted_price = total_price
                
                # Update the bundle's price
                self.treestore.set_value(bundle_iter, 2, float(discounted_price))
                self.treestore.set_value(bundle_iter, 3, float(total_price))
                
        except Error as e:
            print(f"Error loading bundles: {e}")
            self.show_error_dialog(f"Error loading bundles: {e}")

    def load_standalone_products(self, cursor):
        """Load all products as standalone items, regardless of bundle membership"""
        try:
            # Get all products
            query = "SELECT Name, Price, Stock FROM product"
            cursor.execute(query)
            products = cursor.fetchall()
            
            # Add each product as a top-level node
            for product in products:
                product_name = product['Name']
                product_price = float(product['Price']) if product['Price'] is not None else 0.0
                
                # Add as top-level node with empty discount and "product" type
                # Format: Name, Discount, Price, Original Price, Type
                self.treestore.append(None, [product_name, "", product_price, product_price, "product"])
                
        except Error as e:
            print(f"Error loading standalone products: {e}")
            self.show_error_dialog(f"Error loading products: {e}")

    def process_and_add_data(self, rows):
        """Process rows from the database and add them to the ListStore"""
        for row in rows:
            converted_row = []
            
            for attr_info in self.attributes_to_display:
                column_name = attr_info[0]
                expected_type = attr_info[3]
                
                # Get the value from the dictionary row
                value = row.get(column_name)
                
                # Convert using our improved method
                converted_value = self.convert_value(value, expected_type, column_name)
                converted_row.append(converted_value)
            
            self.liststore.append(converted_row)
        
        # Update the filter if it exists
        if hasattr(self, 'filter_model') and self.filter_model:
            self.filter_model.refilter()
    
    def convert_value(self, value, expected_type, column_name):
        """Convert a database value to the expected Python type with special handling for price"""
        if value is None:
            # Handle NULL values
            if expected_type == str:
                return ""
            elif expected_type in (float, int):
                return 0
            else:
                return None
        
        try:
            # Special handling for Price column
            if column_name == "Price":
                # Handle various price formats
                if isinstance(value, str):
                    # Remove any currency symbols or commas
                    cleaned_value = value.replace('$', '').replace(',', '').strip()
                    return float(cleaned_value)
                elif isinstance(value, (float, int, bool)):
                    # Direct conversion for numeric types
                    return float(value)
                else:
                    print(f"Unexpected Price value type: {type(value)}")
                    return 0.0
            else:
                # Normal conversion for other columns
                return expected_type(value)
        except (ValueError, TypeError) as e:
            print(f"Conversion error for {column_name}: {value} to {expected_type.__name__}: {e}")
            # Return appropriate default value
            if expected_type == str:
                return ""
            elif expected_type == float:
                return 0.0
            elif expected_type == int:
                return 0
            else:
                return None
    
    def on_add_to_cart_clicked(self, button):
        """Handle Add to Cart button click"""
        # Check if there's a selection in the browse_tree
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        
        if treeiter is None:
            self.show_error_dialog("Please select a product or bundle first")
            return
        
        # Get data from the selected row
        # If using filter model, we need to convert iter to the base model
        if hasattr(self, 'filter_model') and self.filter_model:
            # Convert the iter from filter model to the base model
            child_iter = self.filter_model.convert_iter_to_child_iter(treeiter)
            item_name = self.treestore.get_value(child_iter, 0)
            item_price = self.treestore.get_value(child_iter, 2)
            item_type = self.treestore.get_value(child_iter, 4)
            
            # Check if this is a bundle by looking at the type column
            is_bundle = item_type.startswith("bundle-")
        else:
            item_name = model.get_value(treeiter, 0)
            item_price = model.get_value(treeiter, 2)
            item_type = model.get_value(treeiter, 4)
            is_bundle = item_type.startswith("bundle-")
        
        # Get the quantity
        quantity = self.quantity_selector.get_value_as_int()
        if quantity <= 0:
            self.show_error_dialog("Please specify a quantity greater than zero")
            return
        
        # Calculate the total for this item
        total_price = item_price * quantity
        
        if is_bundle:
            # For bundles, we need special handling
            self.add_bundle_to_cart(item_name, item_price, quantity, total_price, child_iter if hasattr(self, 'filter_model') else treeiter, model)
        else:
            # For regular products, check if it's already in cart
            self.add_product_to_cart(item_name, item_price, quantity, total_price, "", "product")
        
        # Reset the quantity spinner to 1
        self.quantity_selector.set_value(1)

    def add_product_to_cart(self, product_name, product_price, quantity, total_price, parent_name, item_type):
        """Add a standalone product to the cart"""
        # Print debug info
        print(f"Adding product: {product_name}, price: {product_price}, quantity: {quantity}, total: {total_price}")
        
        # Ensure prices are floats
        product_price_float = float(product_price) if product_price is not None else 0.0
        total_price_float = float(total_price) if total_price is not None else 0.0
        
        # Check if this product is already in the cart as a standalone item
        product_in_cart = False
        
        # Iterate through top-level items in cart
        for row in self.cart_treestore:
            if row[0] == product_name and row[4] == item_type and row[5] == parent_name:
                # Product is already in cart, update quantity and total
                new_quantity = row[2] + quantity
                new_total = product_price_float * new_quantity
                row[2] = new_quantity
                row[3] = new_total
                product_in_cart = True
                print(f"Updated existing product: quantity={new_quantity}, total=${new_total:.2f}")
                break
        
        # If not in cart already, add new row
        if not product_in_cart:
            self.cart_treestore.append(None, [
                product_name, 
                product_price_float,  # Use float for price
                quantity, 
                total_price_float,  # Use float for total
                item_type, 
                parent_name
            ])
            print(f"Added new product: price=${product_price_float:.2f}, total=${total_price_float:.2f}")
            
    def add_bundle_to_cart(self, bundle_name, bundle_price, quantity, total_price, bundle_iter, model):
        """Add a bundle and its products to the cart"""
        # Print debug info
        print(f"Adding bundle: {bundle_name}, price: {bundle_price}, quantity: {quantity}, total: {total_price}")
        
        # First check if this bundle is already in the cart
        bundle_in_cart = False
        bundle_cart_iter = None
        
        # Iterate through top-level items in cart
        for row in self.cart_treestore:
            if row[0] == bundle_name and row[4] == "bundle":
                # Bundle is already in cart, update quantity and total
                new_quantity = row[2] + quantity
                new_total = bundle_price * new_quantity
                row[2] = new_quantity
                row[3] = new_total
                bundle_in_cart = True
                bundle_cart_iter = row.iter
                print(f"Updated existing bundle: quantity={new_quantity}, total=${new_total:.2f}")
                break
        
        # If bundle not in cart, add it
        if not bundle_in_cart:
            # Ensure bundle_price is a float
            bundle_price_float = float(bundle_price) if bundle_price is not None else 0.0
            total_price_float = float(total_price) if total_price is not None else 0.0
            
            bundle_cart_iter = self.cart_treestore.append(None, [
                bundle_name, 
                bundle_price_float,  # Use float for price
                quantity, 
                total_price_float,  # Use float for total
                "bundle", 
                ""
            ])
            print(f"Added new bundle: price=${bundle_price_float:.2f}, total=${total_price_float:.2f}")
        
        # Now add or update the products in this bundle
        # Get the child model if we're using a filter
        if isinstance(model, Gtk.TreeModelFilter):
            child_model = model.get_model()
        else:
            child_model = model
        
        # Check if bundle has children (products)
        if child_model.iter_has_child(bundle_iter):
            # Add each product in the bundle as a child in the cart
            for i in range(child_model.iter_n_children(bundle_iter)):
                product_iter = child_model.iter_nth_child(bundle_iter, i)
                
                product_name = child_model.get_value(product_iter, 0)
                product_price = child_model.get_value(product_iter, 2)
                
                # Ensure product_price is a float
                product_price_float = float(product_price) if product_price is not None else 0.0
                
                print(f"  Product in bundle: {product_name}, price: ${product_price_float:.2f}")
                
                # Calculate product total
                product_total = product_price_float * quantity
                
                # Check if this product is already under this bundle in the cart
                product_found = False
                
                # If the bundle is already in cart, check its children
                if bundle_in_cart:
                    for j in range(self.cart_treestore.iter_n_children(bundle_cart_iter)):
                        child_iter = self.cart_treestore.iter_nth_child(bundle_cart_iter, j)
                        if self.cart_treestore.get_value(child_iter, 0) == product_name:
                            # Product already under bundle, update quantity
                            new_child_quantity = self.cart_treestore.get_value(child_iter, 2) + quantity
                            new_child_total = product_price_float * new_child_quantity
                            self.cart_treestore.set_value(child_iter, 2, new_child_quantity)
                            self.cart_treestore.set_value(child_iter, 3, new_child_total)
                            product_found = True
                            print(f"    Updated existing product: quantity={new_child_quantity}, total=${new_child_total:.2f}")
                            break
                
                # If product not found under this bundle, add it
                if not product_found:
                    self.cart_treestore.append(bundle_cart_iter, [
                        product_name,
                        product_price_float,  # Use float for price
                        quantity,
                        product_total,  # Calculate total as float
                        "bundle-product",
                        bundle_name
                    ])
                    print(f"    Added new product: price=${product_price_float:.2f}, total=${product_total:.2f}")

    def show_error_dialog(self, message):
        """Show an error dialog with the given message"""
        if not hasattr(self, 'cart_window') or not self.cart_window:
            print(f"Error (no window to show dialog): {message}")
            return
            
        dialog = Gtk.MessageDialog(
            transient_for=self.cart_window,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.run()
        dialog.destroy()

def main():
    app = ProductViewer("main.glade")
    Gtk.main()

if __name__ == "__main__":
    main()