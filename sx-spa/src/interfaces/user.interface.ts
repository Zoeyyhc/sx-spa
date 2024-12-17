export interface User{
    username: string;
    password: string | null;
    display_name: string;
    mobile: string;
    campus: string;
    created_at: string;
    wx?: string;
    uni7?: string;
    permission?: [string];
    ab?: string;
    user_type: string;
}