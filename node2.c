#include <stdio.h>

#define MAXCOST 999

extern struct rtpkt
{
    int sourceid;   // id of router sending this pkt
    int destid;     // id of router to which pkt being sent
    int mincost[4]; // min cost to node 0 ... 3
};

extern int TRACE;
extern int YES;
extern int NO;

struct distance_table 
{
  int costs[4][4];
} dt2;

void rtinit2() 
{
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            dt2.costs[i][j] = MAXCOST;
        }
    }

    // Set direct link costs
    dt2.costs[0][0] = 3;
    dt2.costs[1][1] = 1;
    dt2.costs[2][2] = 0;
    dt2.costs[3][3] = 2;

    struct rtpkt pkt;
    pkt.sourceid = 2;

    for (int i = 0; i < 4; i++)
    {
        int min = MAXCOST;
        for (int j = 0; j < 4; j++)
        {
            if (dt2.costs[i][j] < min)
            {
                min = dt2.costs[i][j];
            }
        }
        pkt.mincost[i] = min;
    }

    // Send to neighbors: 0, 1, 3
    pkt.destid = 0;
    tolayer2(pkt);

    pkt.destid = 1;
    tolayer2(pkt);

    pkt.destid = 3;
    tolayer2(pkt);
}


void rtupdate2(rcvdpkt) struct rtpkt *rcvdpkt;
{
    int src = rcvdpkt->sourceid;
    int updated = 0;

    // Get the direct link cost to the source
    int direct_link_cost;
    switch (src) {
        case 0: direct_link_cost = 3; break;
        case 1: direct_link_cost = 1; break;
        case 3: direct_link_cost = 2; break;
        default: return; // Not a direct neighbor, ignore
    }

    // Update cost table entries for each destination
    for (int i = 0; i < 4; i++)
    {
        // Calculate the new cost to reach node i through the source
        int new_cost = direct_link_cost + rcvdpkt->mincost[i];

        // If the new cost is less than the current cost, update it
        if (new_cost < dt2.costs[src][i])
        {
            dt2.costs[src][i] = new_cost;
            updated = 1;
        }
    }

    if (updated)
    {
        // Send updated costs to neighbors
        struct rtpkt pkt;
        pkt.sourceid = 2;

        for (int i = 0; i < 4; i++)
        {
            int min = MAXCOST;
            for (int j = 0; j < 4; j++)
            {
                if (dt2.costs[j][i] < min)
                {
                    min = dt2.costs[j][i];
                }
            }
            pkt.mincost[i] = min;
        }

        // Send to neighbors: 0, 1, 3
        pkt.destid = 0;
        tolayer2(pkt);

        pkt.destid = 1;
        tolayer2(pkt);

        pkt.destid = 3;
        tolayer2(pkt);
    }
}


printdt2(dtptr)
  struct distance_table *dtptr;
  
{
  printf("                via     \n");
  printf("   D2 |    0     1    3 \n");
  printf("  ----|-----------------\n");
  printf("     0|  %3d   %3d   %3d\n",dtptr->costs[0][0],
	 dtptr->costs[0][1],dtptr->costs[0][3]);
  printf("dest 1|  %3d   %3d   %3d\n",dtptr->costs[1][0],
	 dtptr->costs[1][1],dtptr->costs[1][3]);
  printf("     3|  %3d   %3d   %3d\n",dtptr->costs[3][0],
	 dtptr->costs[3][1],dtptr->costs[3][3]);
}

