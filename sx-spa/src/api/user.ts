import axios from "../utils/http";
import type {User} from "@/interfaces/user.interface";

export const getCurrentUser = async () => {
    const response = await axios.get<User>('/auth');
    return response.data;
}