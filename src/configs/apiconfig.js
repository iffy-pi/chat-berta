// api configuration used in the React Front End
const CHAT_BERTA_API = `${(process.env.NODE_ENV === 'development') ? 'http://localhost:5000' : 'https://chat-berta-api.vercel.app' }/api`
export {
    CHAT_BERTA_API
}