import request from "@/http";
import type {ChatData} from "@/schema/Chat";

//  get请求，没参数，
export const startChat = (user_id:number, chat: ChatData): any =>{
    return request.post(`/chat/get_chat/${user_id}`, chat);
}
