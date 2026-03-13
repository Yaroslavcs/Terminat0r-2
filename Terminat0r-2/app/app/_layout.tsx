import { Stack } from "expo-router";

export default function Layout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: "#1a1a2e" },
        headerTintColor: "#eaeaea",
      }}
    >
      <Stack.Screen name="index" options={{ title: "lifehack", headerShown: false }} />
      <Stack.Screen name="quest-create" options={{ title: "квести" }} />
      <Stack.Screen name="quest/[id]" options={{ title: "квест" }} />
      <Stack.Screen name="camera" options={{ title: "верифікація" }} />
      <Stack.Screen name="stats" options={{ title: "статистика" }} />
    </Stack>
  );
}
