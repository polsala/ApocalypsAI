#[cfg(test)]\nmod tests {\n    use scavenger_knapsack::solve;\n\n    #[test]\n    fn sample_case() {\n        let input = "\
10\n\
gold 5 10\n\
silver 4 7\n\
food 3 4\n\
water 2 3\n";\n        let expected = "17\ngold silver";\n        let output = solve(input);\n        assert_eq!(output.trim(), expected);\n    }\n}\n
