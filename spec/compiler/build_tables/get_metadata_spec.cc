#include "compiler/compiler_spec_helper.h"
#include "compiler/rules/metadata.h"
#include "compiler/build_tables/get_metadata.h"

using namespace rules;
using namespace build_tables;

START_TEST

describe("getting metadata for rules", []() {
    MetadataKey key1 = MetadataKey(100);
    MetadataKey key2 = MetadataKey(101);
    rule_ptr rule;

    describe("when given a metadata rule", [&]() {
        before_each([&]() {
            rule = make_shared<Metadata>(sym("x"), map<MetadataKey, int>({
                { key1, 1 },
                { key2, 2 },
            }));
        });

        it("returns the value for the given key", [&]() {
            AssertThat(get_metadata(rule, key1), Equals(1));
            AssertThat(get_metadata(rule, key2), Equals(2));
        });

        it("returns 0 if the rule does not have the key", [&]() {
            AssertThat(get_metadata(rule, MetadataKey(0)), Equals(0));
        });

        describe("when the rule contains another metadata rule", [&]() {
            it("also gets metadata from the inner metadata rule", [&]() {
                rule = make_shared<Metadata>(make_shared<Metadata>(sym("x"), map<MetadataKey, int>({
                    { key1, 1 }
                })), map<MetadataKey, int>());

                AssertThat(get_metadata(rule, key1), Equals(1));
            });
        });
    });

    describe("when given a non-metadata rule", [&]() {
        it("returns 0", [&]() {
            auto rule = sym("x");
            AssertThat(get_metadata(rule, key1), Equals(0));
        });
    });
});

END_TEST
