// rotohist/frontend/app/page.tsx

interface User {
  id: number;
  name: string;
}

async function fetchUsers(): Promise<User[]> {
  const res = await fetch("http://localhost:8000/api/users", {
    // Server-side fetch: don't cache during dev
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch users");
  }

  return res.json();
}

export default async function Page() {
  const users = await fetchUsers();

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Users</h1>
      <ul className="list-disc pl-6">
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}

