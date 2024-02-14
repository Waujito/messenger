import { AS_URL } from "../app";
import { getAxiosInstance } from "../microservices/api";

export default function () {
  return getAxiosInstance(AS_URL());
}
