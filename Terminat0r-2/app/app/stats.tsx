import { useState, useEffect } from "react";
import { View, Text, StyleSheet, ActivityIndicator } from "react-native";
import { useDeviceId } from "../hooks/useDeviceId";
import { api } from "../services/api";

export default function StatsScreen() {
  const [stats, setStats] = useState<{ gold: number; xp: number; level: number } | null>(null);

  const deviceId = useDeviceId();

  useEffect(() => {
    api.getStats(deviceId).then(setStats).catch(() => setStats({ gold: 0, xp: 0, level: 1 }));
  }, []);

  if (stats === null) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#e94560" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.label}>gold</Text>
        <Text style={styles.value}>{stats.gold}</Text>
      </View>
      <View style={styles.card}>
        <Text style={styles.label}>xp</Text>
        <Text style={styles.value}>{stats.xp}</Text>
      </View>
      <View style={styles.card}>
        <Text style={styles.label}>level</Text>
        <Text style={styles.value}>{stats.level}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#1a1a2e", padding: 24 },
  center: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#1a1a2e" },
  card: {
    backgroundColor: "#16213e",
    borderRadius: 16,
    padding: 32,
    marginBottom: 16,
    alignItems: "center",
  },
  label: { fontSize: 14, color: "#888", marginBottom: 8 },
  value: { fontSize: 36, fontWeight: "700", color: "#eaeaea" },
});
