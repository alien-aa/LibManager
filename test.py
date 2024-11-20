import unittest
from unittest.mock import MagicMock
from model.manager import LibManager, UserManager, Library
from model.user import User

class TestLibManager(unittest.TestCase):
    def setUp(self):
        self.view = MagicMock()
        self.library = Library(current_user=User (username="test", email="test", password="test",
                                                 admin_flag=True, currently_borrowed=[]))
        self.lib_manager = LibManager(library=self.library, view=self.view)

    def test_add_book(self):
        result = self.lib_manager.add_book(title="Test Book", author_name="Test Author", price=10.0, genre="Fiction")
        self.assertTrue(result)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Book")
        self.assertEqual(self.library.books[0].author, "Test Author")

    def test_edit_book(self):
        self.lib_manager.add_book(title="Original Book", author_name="Original Author", price=15.0, genre="Fiction")
        result = self.lib_manager.edit_book(old_title="Original Book", old_author="Original Author", old_price=15.0,
                                            old_genre="Fiction",
                                            title="Edited Book", author="Edited Author", price=20.0,
                                            genre="Non-Fiction")
        self.assertTrue(result)
        self.assertEqual(self.library.books[0].title, "Edited Book")
        self.assertEqual(self.library.books[0].author, "Edited Author")
        self.assertEqual(self.library.books[0].price, 20.0)
        self.assertEqual(self.library.books[0].genre, "Non-Fiction")

    def test_delete_book(self):
        self.lib_manager.add_book(title="Book to Delete", author_name="Author", price=10.0, genre="Fiction")
        result = self.lib_manager.delete_book(title="Book to Delete", author="Author", price=10.0, genre="Fiction",
                                              copies=1)
        self.assertTrue(result)
        self.assertEqual(len(self.library.books), 0)

    def test_reserve_book_success(self):
        self.lib_manager.add_book(title="Reservable Book", author_name="Reservable Author", price=10.0, genre="Fiction")
        result = self.lib_manager.reserve_book(title="Reservable Book", author_name="Reservable Author", price=10.0, genre="Fiction")
        self.assertTrue(result)
        self.assertEqual(len(self.library.current_user.currently_borrowed), 1)
        self.assertEqual(self.library.current_user.currently_borrowed[0].title, "Reservable Book")

    def test_reserve_book_not_logged_in(self):
        self.library.current_user = None  # Удаляем текущего пользователя
        result = self.lib_manager.reserve_book(title="Some Book", author_name="Some Author", price=10.0, genre="Fiction")
        self.assertFalse(result)
        self.view.show_error.assert_called_with("You could not reserve book without logging in")

    def test_return_book_success(self):
        self.lib_manager.add_book(title="Returnable Book", author_name="Returnable Author", price=10.0, genre="Fiction")
        self.lib_manager.reserve_book(title="Returnable Book", author_name="Returnable Author", price=10.0, genre="Fiction")
        result = self.lib_manager.return_book(title="Returnable Book", author_name="Returnable Author", price=10.0, genre="Fiction")
        self.assertTrue(result)
        self.assertEqual(len(self.library.current_user.currently_borrowed), 0)

    def test_return_book_not_reserved(self):
        self.lib_manager.add_book(title="Unreserved Book", author_name="Unreserved Author", price=10.0, genre="Fiction")
        result = self.lib_manager.return_book(title="Unreserved Book", author_name="Unreserved Author", price=10.0, genre="Fiction")
        self.assertFalse(result)
        self.view.show_error.assert_called_with("The book was not reserved by this user.")

    def test_show_books_empty(self):
        result = self.lib_manager.show_books(title="Nonexistent Book", author="Nonexistent Author")
        self.assertFalse(result)
        self.view.show_msg.assert_called_with("Empty book list.")

    def test_show_authors_page_not_found(self):
        result = self.lib_manager.show_authors_page(author="Nonexistent Author")
        self.assertFalse(result)
        self.view.show_msg.assert_called_with("Author not found.")

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.view = MagicMock()
        self.provider = MagicMock()
        self.library = Library(users=[], current_user=None)
        self.user_manager = UserManager(library=self.library, view=self.view, provider=self.provider)

    def test_login_success(self):
        user = User(username="testuser", email="test@example.com", password="securepassword")
        self.library.users.append(user)

        result = self.user_manager.login("testuser", "securepassword")

        self.assertTrue(result)
        self.assertEqual(self.library.current_user, user)
        self.view.show_msg.assert_called_with("User testuser has successfully logged in.")

    def test_login_user_not_found(self):
        result = self.user_manager.login("unknown", "password")

        self.assertFalse(result)
        self.view.show_error.assert_called_with("User not found.")

    def test_login_wrong_password(self):
        user = User(username="testuser", email="test@example.com", password="securepassword")
        self.library.users.append(user)

        result = self.user_manager.login("testuser", "wrongpassword")

        self.assertFalse(result)
        self.view.show_error.assert_called_with("Wrong password.")

    def test_logout_success(self):
        user = User(username="testuser", email="test@example.com", password="securepassword")
        self.library.current_user = user

        result = self.user_manager.logout()

        self.assertTrue(result)
        self.assertIsNone(self.library.current_user)
        self.view.show_msg.assert_called_with("User testuser has successfully logged out.")

    def test_logout_no_user(self):
        result = self.user_manager.logout()

        self.assertFalse(result)
        self.view.show_error.assert_called_with("User is not logged in.")

    def test_new_user_success(self):
        result = self.user_manager.new_user("newuser", "newuser@example.com", False, "newpassword")

        self.assertTrue(result)
        new_user = self.library.users[-1]
        self.assertEqual(new_user.username, "newuser")
        self.assertEqual(self.library.current_user, new_user)
        self.view.show_msg.assert_called_with("User newuser has successfully registered and logged in.")

    def test_new_user_already_logged_in(self):
        user = User(username="testuser", email="test@example.com", password="securepassword")
        self.library.current_user = user

        result = self.user_manager.new_user("newuser", "newuser@example.com", False, "newpassword")

        self.assertFalse(result)
        self.view.show_error.assert_called_with("You already logged in")

    def test_delete_user_success(self):
        user = User(username="testuser", email="test@example.com", password="securepassword")
        self.library.current_user = user
        self.library.users.append(user)

        result = self.user_manager.delete_user()

        self.assertTrue(result)
        self.assertIsNone(self.library.current_user)
        self.assertNotIn(user, self.library.users)
        self.view.show_msg.assert_called_with("User testuser has successfully deleted.")

    def test_delete_user_not_logged_in(self):
        result = self.user_manager.delete_user()

        self.assertFalse(result)
        self.view.show_error.assert_called_with("User is not logged in.")

    def test_update_user(self):
        user = User(username="testuser", email="test@example.com", password="securepassword")
        self.library.current_user = user

        result = self.user_manager.update_user(username="updateduser", email="updated@example.com", password="newpassword")

        self.assertTrue(result)
        self.assertEqual(self.library.current_user.username, "updateduser")
        self.assertEqual(self.library.current_user.email, "updated@example.com")
        self.view.show_msg.assert_called_with("User fields updated successfully.")

if __name__ == '__main__':
    unittest.main()
