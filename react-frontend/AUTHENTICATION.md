# Authentication Setup

This React frontend now includes a complete authentication system that integrates with your FastAPI backend.

## Features

- **JWT-based Authentication**: Secure token-based authentication
- **User Registration**: Create new user accounts with email validation
- **User Login**: Sign in with email and password
- **Protected Routes**: Automatic redirection to login for unauthorized users
- **Persistent Sessions**: Tokens stored in localStorage for session persistence
- **User Profile Display**: Shows user name and email in header
- **Logout Functionality**: Secure logout with token cleanup
- **Responsive Design**: Works on desktop and mobile devices

## API Integration

The authentication system connects to your FastAPI backend endpoints:

- `POST /auth/register` - User registration
- `POST /auth/login` - User login (returns JWT token)
- `GET /auth/me` - Get current user info (requires JWT token)

## Configuration

1. **Environment Variables**: Create a `.env.local` file in the `react-frontend` directory:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

2. **Backend Setup**: Ensure your FastAPI backend is running on the configured URL

## Usage

### Authentication Flow

1. **Registration**: Users can register with email, password, and full name
2. **Login**: After registration, users are redirected to login page
3. **Protected Access**: All main routes require authentication
4. **Session Management**: Tokens are automatically validated and refreshed

### Components

- `AuthContext` - Manages authentication state globally
- `Login` - Login form with validation
- `Register` - Registration form with password confirmation
- `ProtectedRoute` - Wrapper for protected pages
- `Header` - Updated with user info and logout functionality

### Routes

- `/login` - Public login page
- `/register` - Public registration page
- `/` - Protected home page
- `/caregiver-dashboard` - Protected dashboard

## Security Features

- Password validation (minimum 6 characters)
- Email format validation
- JWT token expiration handling
- Automatic token cleanup on logout
- Protected route redirection
- Error handling for authentication failures

## Testing

To test the authentication system:

1. Start your FastAPI backend: `uvicorn main:app --reload`
2. Start the React frontend: `npm start`
3. Navigate to `http://localhost:3000`
4. You'll be redirected to `/login`
5. Register a new account or login with existing credentials
6. Access protected routes after authentication



