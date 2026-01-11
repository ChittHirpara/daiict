import { NextResponse } from 'next/server';

export function middleware(request) {
    const path = request.nextUrl.pathname;

    // If accessing root, and not having a specific cookie (mock check), redirect to /signup
    // Ideally we check for a session token.
    if (path === '/') {
        // For demonstration as per user request "whenever user visits, the signup page first should be open"
        // We will redirect root to signup.
        return NextResponse.redirect(new URL('/signup', request.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: '/',
};
