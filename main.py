import gi
import mysql.connector
from mysql.connector import Error
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
        self.customer_window = self.builder.get_object("customer_window")
        if not self.customer_window:
            print("Error: Could not find window with ID 'customer_window'")
            return
            
        self.cart_window = self.builder.get_object("cart_window")
        if not self.cart_window:
            print("Error: Could not find window with ID 'cart_window'")
            
        self.browse_window = self.builder.get_object("browse_window")
        if not self.browse_window:
            print("Error: Could not find window with ID 'browse_window'")
        
        # Get customer ID entry and new order button
        self.customerID_entry = self.builder.get_object("customerID_entry")
        if not self.customerID_entry:
            print("Error: Could not find Entry with ID 'customerID_entry'")
        
        self.newOrder_button = self.builder.get_object("newOrder_button")
        if not self.newOrder_button:
            print("Error: Could not find Button with ID 'newOrder_button'")
        else:
            self.newOrder_button.connect("clicked", self.on_newOrder_button_clicked)
        
        # Connect window close signals
        self.customer_window.connect("destroy", Gtk.main_quit)
        if self.cart_window:
            self.cart_window.connect("delete-event", self.on_cart_window_close)
        if self.browse_window:
            self.browse_window.connect("delete-event", self.on_browse_window_close)
        
        # Store customer ID
        self.customer_id = None
        
        # Initialize windows but don't show them yet
        self.initialize_windows()
        
        # Show the customer window
        self.customer_window.show_all()

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
            "host": "192.168.171.222",
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
        if not hasattr(self, 'cart_window') or not self.cart_window:
            print(f"Success: {message}")
            return
            
        dialog = Gtk.MessageDialog(
            transient_for=self.cart_window,
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
        
        # Get the value from the column we're searching on
        value = model.get_value(iter, self.search_attribute_index)
        
        # Convert value to string for searching
        if value is not None:
            value_str = str(value).lower()
            # Return True if the search text is found in the value
            found = search_text in value_str
            
            # If this is a parent node and it matches, show it
            if found:
                return True
                
            # If this is a parent node and it doesn't match, check children
            if model.iter_has_child(iter):
                for i in range(model.iter_n_children(iter)):
                    child = model.iter_nth_child(iter, i)
                    if self.filter_visible_func(model, child, None):
                        return True
            
            # If this is a child node, check if parent matches
            parent = model.iter_parent(iter)
            if parent and self.filter_visible_func(model, parent, None):
                return True
                
            return found
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