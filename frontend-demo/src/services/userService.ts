import request from "@/http";
import type {LoginData, RegisterData} from "@/schema/User";

//  get请求，没参数，
export const test = (): any =>{
    return request.get("/user/test");
}


export const userLogin = (data: LoginData): any =>{
    return request.post("/user/login", data);
}


export const userRegister = (data: RegisterData): any =>{
    return request.post("/user/", data);
}


export const userEdit = (data: RegisterData, userId: number): any =>{
    return request.put(`/user/${userId}`, data);
}

export const getUser = (userId: number): any =>{
    return request.get(`/user/${userId}`);
}
