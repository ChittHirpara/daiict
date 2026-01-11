import dbConnect from '@/veritas1/db/connection';
import User from '@/veritas1/db/User';
import bcrypt from 'bcryptjs';
import { NextResponse } from 'next/server';

export async function POST(request) {
    try {
        await dbConnect();
        const { name, email, password } = await request.json();

        if (!name || !email || !password) {
            return NextResponse.json(
                { message: 'Please provide all fields' },
                { status: 400 }
            );
        }

        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return NextResponse.json(
                { message: 'User already exists' },
                { status: 400 }
            );
        }

        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        const user = await User.create({
            name,
            email,
            password: hashedPassword,
        });

        return NextResponse.json(
            { message: 'User created successfully', user: { id: user._id, name: user.name, email: user.email, role: user.role } },
            { status: 201 }
        );
    } catch (error) {
        console.error('Signup error:', error);
        return NextResponse.json(
            { message: 'Internal Server Error' },
            { status: 500 }
        );
    }
}
