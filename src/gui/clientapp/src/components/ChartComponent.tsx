import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  BarChart,
  Bar,
} from "recharts";
import { IData, IMetrics } from "../Interfaces/metrics.interface";

const ChartComponent = ({ data }: IMetrics) => {
  return (
    <BarChart width={530} height={350} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="standar" fill="#8884d8" />
      <Bar dataKey="extended" fill="#82ca9d" />{" "}
    </BarChart>
  );
};
export default ChartComponent;
