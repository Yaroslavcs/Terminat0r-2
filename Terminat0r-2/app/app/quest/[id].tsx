import { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from "react-native";
import { router, useLocalSearchParams } from "expo-router";
import { useDeviceId } from "../../hooks/useDeviceId";
import { api } from "../../services/api";

type QuestData = {
  quest_id: number;
  title: string;
  monster: string;
  backstory: string;
  reward_gold: number;
  reward_xp: number;
  verification_hint: string;
};

export default function QuestScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [quest, setQuest] = useState<QuestData | null>(null);
  const [loadingQuest, setLoadingQuest] = useState(true);
  const [loading, setLoading] = useState(false);

  const deviceId = useDeviceId();

  useEffect(() => {
    if (!id) return;
    setLoadingQuest(true);
    api
      .getQuest(deviceId, parseInt(id, 10))
      .then((q) => {
        setQuest(q);
        setLoadingQuest(false);
      })
      .catch(() => {
        setQuest({
          quest_id: parseInt(id, 10),
          title: "Failed to load",
          monster: "",
          backstory: "",
          reward_gold: 0,
          reward_xp: 0,
          verification_hint: "",
        });
        setLoadingQuest(false);
      });
  }, [id]);

  async function completeWithPhoto() {
    router.push({ pathname: "/camera", params: { questId: id } });
  }

  async function completeWithoutPhoto() {
    if (!id) return;
    setLoading(true);
    try {
      const res = await api.verifyQuest(deviceId, parseInt(id, 10));
      Alert.alert(
        res.verified ? "Quest complete!" : "Partial success",
        `${res.message}\n+${res.gold_earned} gold, +${res.xp_earned} xp`,
        [{ text: "OK", onPress: () => router.replace("/") }]
      );
    } catch (e) {
      Alert.alert("Error", String(e));
    } finally {
      setLoading(false);
    }
  }

  if (loadingQuest || !quest) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#e94560" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>{quest.title}</Text>
        <Text style={styles.monster}>{quest.monster}</Text>
        <Text style={styles.backstory}>{quest.backstory}</Text>
        <View style={styles.rewards}>
          <Text style={styles.reward}>+{quest.reward_gold} gold</Text>
          <Text style={styles.reward}>+{quest.reward_xp} xp</Text>
        </View>
        <Text style={styles.hint}>{quest.verification_hint}</Text>
      </View>

      <TouchableOpacity
        style={[styles.btn, styles.btnPrimary]}
        onPress={completeWithPhoto}
        disabled={loading}
      >
        <Text style={styles.btnText}>verify with camera</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.btn, styles.btnSecondary]}
        onPress={completeWithoutPhoto}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#0f3460" />
        ) : (
          <Text style={styles.btnTextSecondary}>done (no photo)</Text>
        )}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#1a1a2e", padding: 24 },
  card: {
    backgroundColor: "#16213e",
    borderRadius: 16,
    padding: 24,
    marginBottom: 32,
    borderWidth: 1,
    borderColor: "#0f3460",
  },
  title: { fontSize: 22, fontWeight: "700", color: "#eaeaea", marginBottom: 8 },
  monster: { fontSize: 16, color: "#e94560", marginBottom: 12 },
  backstory: { fontSize: 15, color: "#aaa", lineHeight: 22, marginBottom: 16 },
  rewards: { flexDirection: "row", gap: 16, marginBottom: 12 },
  reward: { fontSize: 14, color: "#4ade80", fontWeight: "600" },
  hint: { fontSize: 13, color: "#666" },
  btn: {
    borderRadius: 12,
    padding: 18,
    alignItems: "center",
    marginBottom: 12,
  },
  btnPrimary: { backgroundColor: "#e94560" },
  btnSecondary: { backgroundColor: "#16213e", borderWidth: 1, borderColor: "#0f3460" },
  btnText: { color: "#fff", fontSize: 18, fontWeight: "600" },
  btnTextSecondary: { color: "#0f3460", fontSize: 18, fontWeight: "600" },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#1a1a2e",
  },
});
