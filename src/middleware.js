import { NextResponse } from 'next/server';

export function middleware(request) {
    const path = request.nextUrl.pathname;

    // Check for auth cookie
    const authToken = request.cookies.get('auth_token')?.value;

    if (path === '/') {
        // If valid auth token exists, let them pass to dashboard
        if (authToken) {
            return NextResponse.next();
        }
        // Otherwise redirect to signup
        return NextResponse.redirect(new URL('/signup', request.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: '/',
};
