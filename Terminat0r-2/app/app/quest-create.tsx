import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import { router } from "expo-router";
import { useDeviceId } from "../hooks/useDeviceId";
import { api } from "../services/api";

export default function QuestCreate() {
  const [task, setTask] = useState("");
  const [loading, setLoading] = useState(false);
  const deviceId = useDeviceId();

  async function createQuest() {
    if (!task.trim()) return;
    setLoading(true);
    try {
      const res = await api.generateQuest(deviceId, task.trim());
      router.push({ pathname: "/quest/[id]", params: { id: String(res.quest_id) } });
    } catch (e) {
      Alert.alert("Помилка", String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>створити квест</Text>
      <Text style={styles.subtitle}>що потрібно зробити?</Text>

      <TextInput
        style={styles.input}
        placeholder="наприклад: прибрати кімнату, випити воду"
        placeholderTextColor="#666"
        value={task}
        onChangeText={setTask}
        multiline
      />

      <TouchableOpacity
        style={[styles.btn, loading && styles.btnDisabled]}
        onPress={createQuest}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.btnText}>створити</Text>
        )}
      </TouchableOpacity>

      <TouchableOpacity onPress={() => router.back()}>
        <Text style={styles.back}>назад</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#1a1a2e" },
  content: { padding: 24, paddingTop: 48 },
  title: { fontSize: 28, fontWeight: "700", color: "#eaeaea", marginBottom: 8 },
  subtitle: { fontSize: 16, color: "#888", marginBottom: 32 },
  input: {
    backgroundColor: "#16213e",
    borderRadius: 12,
    padding: 16,
    color: "#eaeaea",
    fontSize: 16,
    minHeight: 100,
    marginBottom: 24,
  },
  btn: {
    backgroundColor: "#0f3460",
    borderRadius: 12,
    padding: 18,
    alignItems: "center",
    marginBottom: 16,
  },
  btnDisabled: { opacity: 0.7 },
  btnText: { color: "#fff", fontSize: 18, fontWeight: "600" },
  back: { color: "#e94560", fontSize: 16, textAlign: "center" },
});
