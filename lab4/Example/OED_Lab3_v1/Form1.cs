using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace OED_Lab3_v1
{
    public partial class Form1 : Form
    {
        public static double[] X = new double[] { 1, 3, 5, 7, 9, 11, 13, 15, 17 };
        public static double[] Y = new double[] { 12.5, 17.5, 22.5, 27.5, 32.5, 37.5 };
        public static double[,] Nij = new double[,]
        {
            {3, 3, 0, 0, 0, 0, 0, 0, 0 },
            {0, 7, 1, 4, 0, 0, 0, 0, 0 },
            {0, 4, 7, 1, 0, 0, 0, 0, 0 },
            {0, 0, 4, 9, 0, 0, 0, 0, 0 },
            {0, 0, 1, 7, 5, 6, 7, 0, 0 },
            {0, 0, 0, 0, 1, 2, 0, 1, 2 },
        };
        public static int nXlenght = X.Length;
        public static int nYlenght = Y.Length;
        public static double[] Nx = new double[nXlenght];
        public static double[] Ny = new double[nYlenght];
        public static double Nxy;


        public static double[] Y_x = new double[nXlenght];


        public static double[] NxX = new double[nXlenght];
        public static double[] NxX2 = new double[nXlenght];
        public static double[] NyY = new double[nYlenght];
        public static double[] NxyXY = new double[nXlenght];


        public static double a0, a1;
        public static double N1a0, N1a1, s1, N2a0, N2a1, s2;


        public static int n;//Объём выборки
        public static double NijMAX; //Максимальный элемент матрицы
        public static double C1_m0x, C2_m0y;
        public static double h1, h2;//шаг X и Y
        public static double[] ui = new double[nXlenght], vj = new double[nYlenght];


        public static double U_, U2_, V_, V2_, Su, Sv;
        public static double[,] tab30Up = new double[,]
        {
            {3, 3, 0, 0, 0, 0, 0, 0, 0 },
            {0, 7, 1, 4, 0, 0, 0, 0, 0 },
            {0, 4, 7, 1, 0, 0, 0, 0, 0 },
            {0, 0, 4, 9, 0, 0, 0, 0, 0 },
            {0, 0, 1, 7, 5, 6, 7, 0, 0 },
            {0, 0, 0, 0, 1, 2, 0, 1, 2 },
        };
        public static double[,] tab30Down = new double[,]
        {
            {0, 0, 0, 0, 0, 0, 0, 0, 0 },
            {0, 0, 0, 0, 0, 0, 0, 0, 0 },
            {0, 0, 0, 0, 0, 0, 0, 0, 0 },
            {0, 0, 0, 0, 0, 0, 0, 0, 0 },
            {0, 0, 0, 0, 0, 0, 0, 0, 0 },
            {0, 0, 0, 0, 0, 0, 0, 0, 0 },
        };
        public static double rv, x_, y_, Sx, Sy;

        public static double[] tab30Bottom = new double[nXlenght], tab30Right = new double[nYlenght];
        public static double tab30FullSum;

        public static double th, tak, FH, Q, QR, Qe, k1, k2, FT;
        public static double[] YiMinusY_ = new double[nYlenght], YiMinusY_2 = new double[nYlenght], Y_XiMinusY_ = new double[nXlenght], Y_XiMinusY_2 = new double[nXlenght];

        public struct Uravn
        {
            public double NumPart;
            public double xyPart;
        }

        public Uravn _Yx, _Xy;

        public Form1()
        {
            InitializeComponent();

            NxNyCalc();
            CalcY_X();
            CalcTable28();
            CalcSystem();
            Slide14();
            Slide16();
            CreateTab30();
            DrawTable30();
            Slide19();
            Last();
            GraphRis10Draw();
            LabelsDraw();
        }

        //Рассчёт сумм для начальных данных
        public void NxNyCalc()
        {
            //Расчёт NX
            for(int i = 0; i < Nx.Length; i++)
            {
                for(int j = 0; j < Ny.Length; j++)
                {
                    Nx[i] += Nij[j, i];
                }
            }
            //Расчёт NY
            for (int i = 0; i < Ny.Length; i++)
            {
                for (int j = 0; j < Nx.Length; j++)
                {
                    Ny[i] += Nij[i, j];
                }
            }
            //Расчёт Nxy
            Nxy = Nx.Sum();
        }

        public void CalcY_X()
        {
            double tempSum = 0;
            for (int i = 0; i < Nx.Length; i++)
            {
                for (int j = 0; j < Ny.Length; j++)
                {
                    tempSum += Nij[j, i] * Y[j];
                }
                Y_x[i] = tempSum / Nx[i];
                tempSum = 0;
            }
        }

        public void CalcTable28()
        {
            for(int i = 0; i < NxX.Length; i++)
            {
                NxX[i] = X[i] * Nx[i];
                NxX2[i] = Nx[i] * Math.Pow(X[i], 2);
            }

            for (int i = 0; i < NyY.Length; i++)
            {
                NyY[i] = Y[i] * Ny[i];
            }

            for (int i = 0; i < X.Length; i++)
            {
                for (int j = 0; j < Y.Length; j++)
                {
                    NxyXY[i] += Nij[j, i] * Y[j];
                }
                NxyXY[i] *= X[i];
            }
        }

        public void CalcSystem()
        {
            N1a0 = Nxy;
            N1a1 = N2a0 = NxX[NxX.Length - 1];
            s1 = NyY[NyY.Length - 1];
            N2a1 = NxX2[NxX2.Length - 1];
            s2 = NxyXY[NxyXY.Length - 1];

            double x1, y1, c1, x2, y2, c2; // Переменные, предоставленные в условии.
            double x, y;                   // Переменные, которые нужно найти.
            double b0, c0;                 // Вспомогательные переменные.
            x1 = N1a0; y1 = N1a1; c1 = s1;
            x2 = N2a0; y2 = N2a1; c2 = s2;

            if (Math.Abs(x1 * y2 - x2 * y1) >= 0.0001)
            {
                if (a1 != 0)
                {
                    b0 = y2 - (y1 / x1 * x2);
                    c0 = -(c2 - (c1 / x1 * x2));
                    y = c0 / b0;
                    x = (-c1 - ((y1 * c0) / b0)) / a1;

                    a0 = Math.Abs(x);
                    a1 = Math.Abs(y);
                }
                else
                {
                    b0 = y1 - (y2 / x2 * x1);
                    c0 = -(c1 - (c2 / x2 * x1));
                    y = c0 / b0;
                    x = (-c2 - ((y2 * c0) / b0)) / x2;

                    a0 = Math.Abs(x);
                    a1 = Math.Abs(y);
                }
            }
            else
            {
                MessageBox.Show("н(ЕА)т");
            }                     
        }

        public void Slide14()
        {
            n = Nij.Length;
            NijMAX = Nij.Cast<double>().Max();

            C1_m0x = Nx.Max();
            for (int i = 0; i < X.Length; i++)
            {
                if (Nx[i] == C1_m0x)
                {
                    C1_m0x = X[i];
                    break;
                }
            }

            C2_m0y = Ny.Max();
            for (int i = 0; i < Y.Length; i++)
            {
                if (Ny[i] == C2_m0y)
                {
                    C2_m0y = Y[i];
                    break;
                }
            }

            h1 = X[1] - X[0]; // шаг X
            h2 = Y[1] - Y[0]; // шаг Y


            for (int i = 0; i < ui.Length; i++)
            {
                ui[i] = X[i] - C1_m0x;
                ui[i] /= h1;
            }
            for (int j = 0; j < vj.Length; j++)
            {
                vj[j] = Y[j] - C2_m0y;
                vj[j] /= h2;
            }
        }

        public void Slide16()
        {
            double OneDelN = n;
            OneDelN = 1 / OneDelN;
            U_ = V_ = U2_ = V2_ = 0;            
            
            for(int i = 0; i < ui.Length; i++)
            {
                U_ += Nx[i] * ui[i];                
            }
            U_ *= OneDelN;

            for (int j = 0; j < vj.Length; j++)
            {
                V_ += Ny[j] * vj[j];
            }
            V_ *= OneDelN;

            for (int i = 0; i < ui.Length; i++)
            {
                U2_ += Nx[i] * Math.Pow(ui[i], 2);
            }
            U2_ *= OneDelN;

            for (int j = 0; j < vj.Length; j++)
            {
                V2_ += Ny[j] * Math.Pow(vj[j], 2);
            }
            V2_ *= OneDelN;

            Su = Math.Sqrt(U2_ - Math.Pow(U_, 2));
            Sv = Math.Sqrt(V2_ - Math.Pow(V_, 2));
        }

        public void CreateTab30()
        {           
            int indexX0 = 0, indexY0 = 0;
            for (int i = 0; i < nXlenght; i++)
            {
                if (ui[i] == 0)
                {
                    indexX0 = i;
                    break;
                }
            }
            for (int j = 0; j < nYlenght; j++)
            {
                if (vj[j] == 0)
                {
                    indexY0 = j;
                    break;
                }
            }

            for (int i = 0; i < nYlenght; i++)
            {
                tab30Up[i, indexX0] = 0;
            }
            for (int i = 0; i < nXlenght; i++)
            {
                tab30Up[indexY0, i] = 0;
            }        
            
            for (int i = 0; i < nYlenght; i++)
            {
                for (int j = 0; j < nXlenght; j++)
                {
                    if (tab30Up[i, j] != 0)
                    {
                        tab30Down[i, j] = vj[i] * ui[j];
                    }
                }
            }

            
            for (int i = 0; i < Nx.Length; i++)
            {
                for (int j = 0; j < Ny.Length; j++)
                {
                    tab30Bottom[i] += tab30Up[j, i] * tab30Down[j, i];
                }
            }
            
            for (int i = 0; i < Ny.Length; i++)
            {
                for (int j = 0; j < Nx.Length; j++)
                {
                    tab30Right[i] += tab30Up[i, j] * tab30Down[i, j];
                }
            }
            
            tab30FullSum = tab30Right.Sum();
        }

        public void DrawTable30()
        {
            dataGridViewT30_1.RowCount = tab30Up.GetLength(0);
            dataGridViewT30_1.ColumnCount = tab30Up.GetLength(1);
            for (int i = 0; i < nYlenght; i++)
            {
                for (int j = 0; j < nXlenght; j++)
                {
                    dataGridViewT30_1.Rows[i].Cells[j].Value = tab30Up[i, j];
                }
            }
            dataGridViewT30_2.RowCount = tab30Down.GetLength(0);
            dataGridViewT30_2.ColumnCount = tab30Down.GetLength(1);
            for (int i = 0; i < nYlenght; i++)
            {
                for (int j = 0; j < nXlenght; j++)
                {
                    dataGridViewT30_2.Rows[i].Cells[j].Value = tab30Down[i, j];
                }
            }

            dataGridViewT30_U.ColumnCount = ui.Length;
            dataGridViewT30_U.RowCount = 1;
            for (int i = 0; i < ui.Length; i++)
            {
                dataGridViewT30_U[i, 0].Value = ui[i];
            }

            dataGridViewT30_V.ColumnCount = 1;
            dataGridViewT30_V.RowCount = vj.Length;
            for (int i = 0; i < vj.Length; i++)
            {
                dataGridViewT30_V[0, i].Value = vj[i];
            }

            dataGridViewT30_B.ColumnCount = ui.Length;
            dataGridViewT30_B.RowCount = 1;
            for (int i = 0; i < tab30Bottom.Length; i++)
            {
                dataGridViewT30_B[i, 0].Value = tab30Bottom[i];
            }

            dataGridViewT30_Right.ColumnCount = 1;
            dataGridViewT30_Right.RowCount = tab30Right.Length;
            for (int i = 0; i < tab30Right.Length; i++)
            {
                dataGridViewT30_Right[0, i].Value = tab30Right[i];
            }
            lblTab30AllSum.Text = tab30FullSum.ToString();
        }

        public void Slide19()
        {
            rv = (tab30FullSum - n * U_ * V_);
            rv /= n * Su * Sv;

            x_ = U_ * h1 + C1_m0x;
            y_ = V_ * h2 + C2_m0y;
            Sx = Su * h1;
            Sy = Sv * h2;


            labelRV.Text = "rв = " + Math.Round(rv,2).ToString();
            labelX_.Text = "_x = " + Math.Round(x_, 2).ToString();
            labelY_.Text = "_y = " + Math.Round(y_, 2).ToString();
            labelSx.Text = "Sx = " + Math.Round(Sx, 2).ToString();
            labelSy.Text = "Sy = " + Math.Round(Sy, 2).ToString();
        }

        public void Last()
        {
            th = Math.Abs(rv) * Math.Sqrt(n - 2);
            th /= Math.Sqrt(1 - rv * rv);

            tak = 2.01;

            for(int i = 0; i < YiMinusY_.Length; i++)
            {
                YiMinusY_[i] = Y[i] - y_;
                YiMinusY_2[i] = Math.Pow(YiMinusY_[i], 2);
            }
            Q = YiMinusY_2.Sum();

            for (int i = 0; i < Y_XiMinusY_.Length; i++)
            {
                Y_XiMinusY_[i] = Y_x[i] - y_;
                Y_XiMinusY_2[i] = Math.Pow(Y_XiMinusY_[i], 2);
            }
            QR = Y_XiMinusY_2.Sum();

            Qe = Q - QR;

            FH = (QR * (n - 2));
            FH /= Qe * (4 - 1);
        }

        public void LabelsDraw()
        {
            label_Yx.Text = "_Yx = " + Math.Round(_Yx.xyPart,6).ToString() + "x + " + Math.Round(_Yx.NumPart,6).ToString();
            label_Xy.Text = "_Xy = " + Math.Round(_Xy.xyPart,6).ToString() + "y + " + Math.Round(_Xy.NumPart,6).ToString();

            label_Th.Text = "tH = " + Math.Round(th, 2).ToString();
            label_Fh.Text = "FH = " + Math.Round(FH, 2).ToString();

            label_QR.Text = "QR = " + Math.Round(QR, 2).ToString();
            label_Qe.Text = "Qe = " + Math.Round(Qe, 2).ToString();

            label_U_.Text = "u_ = " + Math.Round(U_, 2).ToString();
            label_U2_.Text = "u^2_ = " + Math.Round(U2_, 2).ToString();
            label_V_.Text = "v_ = " + Math.Round(V_, 2).ToString();
            label_V2_.Text = "v^2_ = " + Math.Round(V2_, 2).ToString();

            label_Su.Text = "Su = " + Math.Round(Su, 2).ToString();
            label_Sv.Text = "Sv = " + Math.Round(Sv, 2).ToString();

            labelSl22.Text = Math.Round(th, 2).ToString() + " > " + tak.ToString();
        }

        public void GraphRis10Draw()
        {
            double[] Ay = new double[nXlenght];
            double[] Bx = new double[nXlenght];

            _Yx.xyPart = a0;
            _Yx.NumPart = a1;

            _Xy.xyPart = rv * (Sx / Sy);
            _Xy.NumPart = x_ - y_;

            for (int i = 0; i < Ay.Length; i++)
            {
                Ay[i] = _Yx.xyPart * X[i] + _Yx.NumPart;
            }

            //for (int i = 0; i < Ay.Length; i++)
            //{
            //    Ay[i] = _Yx.xyPart * X[i] + _Yx.NumPart;
            //    Bx[i] = _Xy.xyPart * Y[i] + _Xy.NumPart;
            //}

            //for (int i = 0; i < Bx.Length; i++)
            //{
            //    Bx[i] = _Xy.xyPart * Y[i] + _Xy.NumPart;
            //}


            chartRis10.Series[0].Points.Clear();
            chartRis10.Series[0].ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            for (int i = 0; i < nXlenght; i++)
            {
                chartRis10.Series[0].Points.Add(X[i], Y_x[i]);
                chartRis10.Series[1].Points.Add(X[i], Ay[i]);
            }

            //chartRis10.Series[1].Points.Clear();
            //chartRis10.Series[1].ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            //for (int i = 0; i < X.Length; i++)
            //{
            //    chartRis10.Series[1].Points.AddXY(X[i], Ay[i]);
            //}


            //chartRis10.Series[2].Points.Clear();
            //chartRis10.Series[2].ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            //for (int i = 0; i < X.Length; i++)
            //{
            //    chartRis10.Series[2].Points.AddXY(Bx[i], Y[i]);
            //}


            //for(int i = 0; i < Ay.Length; i++)
            //{
            //    Ay[i] = Yx.xyPart * X[i] + Yx.numPart;
            //    Bx[i] = Xy.xyPart * Y[i] + Xy.numPart;
            //}


            //chart_Ris8.Series[0].Points.Clear();
            //chart_Ris8.Series[0].ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            //for (int i = 0; i < X.Length; i++)
            //{
            //    chart_Ris8.Series[0].Points.AddXY(X[i], Y[i]);
            //}

            //chart_Ris8.Series[1].Points.Clear();
            //chart_Ris8.Series[1].ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            //for (int i = 0; i < X.Length; i++)
            //{
            //    chart_Ris8.Series[1].Points.AddXY(X[i], Ay[i]);
            //}

            //chart_Ris8.Series[2].Points.Clear();
            //chart_Ris8.Series[2].ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Line;
            //for (int i = 0; i < X.Length; i++)
            //{
            //    chart_Ris8.Series[2].Points.AddXY(Bx[i], Y[i]);
            //}
        }
    }    
}
