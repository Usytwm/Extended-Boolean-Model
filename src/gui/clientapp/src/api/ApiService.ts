import axios from "axios";
import { IQuery } from "../Interfaces/query.interface";
import { IDocument } from "../Interfaces/document.interface";
import { IMetrics } from "../Interfaces/metrics.interface";

const baseURL = "http://localhost:4000/api";

export const getAllQueries = async (): Promise<IQuery[]> => {
  try {
    const response = await axios.get<IQuery[]>(`${baseURL}/allqueries`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener datos:", error);
    throw error;
  }
};

export const searchQuery = async (query: string): Promise<IDocument[]> => {
  try {
    const response = await axios.get<IDocument[]>(`${baseURL}/search/${query}`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener datos:", error);
    throw error;
  }
};

export const searchStandarQuery = async (
  query: string
): Promise<IDocument[]> => {
  try {
    const response = await axios.get<IDocument[]>(
      `${baseURL}/searchstandar/${query}`
    );
    return response.data;
  } catch (error) {
    console.error("Error al obtener datos:", error);
    throw error;
  }
};

export const getMetrics = async (): Promise<IMetrics> => {
  try {
    const response = await axios.get<IMetrics>(`${baseURL}/metrics`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener datos:", error);
    throw error;
  }
};

export const apiService = {
  getAllQueries,
  searchQuery,
  getMetrics,
};
