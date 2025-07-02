import { useAuth } from "./components/authContext";
import { Card, CardHeader } from "./components/ui/card"



function App() {
  const { user } = useAuth()
  console.log(user);
  const greetings = ["Hi there, ", "Hello World! ", "Welcome, ", "Greetings, ", "Salutations, ", "Nice to see you, "];
  return (
    <div>
      <h1 className="text-2xl ">{greetings[Math.floor(Math.random() * greetings.length)]}{user?.username ? <span>{user.username}</span> : null} 👋</h1>
      <div className='flex flex-row'>
          <Card>
            <CardHeader></CardHeader>
          </Card>
        </div>
    </div>
  )
}

export default App
